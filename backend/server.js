const express = require('express');
const cors = require('cors');
const session = require('express-session');
const passport = require('passport');
//const mysql = require('mysql2/promise');
const { Pool } = require('pg');
const GoogleStrategy = require('passport-google-oauth20').Strategy;
require('dotenv').config();


const app = express();

app.use(cors({
  origin: process.env.CLIENT_ORIGIN || 'http://localhost:8080',
  credentials: true,
}));
app.use(express.json());

app.use(session({
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: process.env.NODE_ENV === 'production',
    httpOnly: true,
    maxAge: 7 * 24 * 60 * 60 * 1000
  }
}));

app.use(passport.initialize());
app.use(passport.session());

const pool = new Pool({
//const pool = mysql.createPool({
  user: process.env.DB_USER,
  host: process.env.DB_HOST,
  database: process.env.DB_NAME,
  password: process.env.DB_PASS,
  port: Number(process.env.DB_PORT || 5432),
  //port: Number(process.env.DB_PORT || 3306),
  //waitForConnections: true,
  //connectionLimit: 10,
  //queueLimit: 0,
});

//Google OAuth routes
passport.use(new GoogleStrategy({
  clientID: process.env.GOOGLE_CLIENT_ID,
  clientSecret: process.env.GOOGLE_CLIENT_SECRET,
  callbackURL: '/auth/google/callback' || '/api/v1/auth/google/callback'
}, async (accessToken, refreshToken, profile, done) => {
  try {
    const email  = profile.emails?.[0]?.value
    const name   = profile.displayName
    const avatar = profile.photos?.[0]?.value

    const result = await pool.query(
      `INSERT INTO users (user_email, user_googleid, user_name, user_avatar)
       VALUES ($1, $2, $3, $4)
       ON CONFLICT (user_googleid) DO UPDATE
         SET user_email  = EXCLUDED.user_email,
             user_name   = EXCLUDED.user_name,
             user_avatar = EXCLUDED.user_avatar
       RETURNING *`,
      [email, profile.id, name, avatar]
    );
    return done(null, result.rows[0]);
  } catch (err) {
    return done(err);
  }
  }));

  passport.serializeUser((user, done) => done(null, user.user_id));

  passport.deserializeUser(async (id, done) => {
    try {
      const result = await pool.query(
        'SELECT * FROM users WHERE user_id = $1', [id]
      );
      done(null, result.rows[0] || null);
    }catch (err) {
      done(err);
    }
  });

  //Auth Middleware
  function requireAuth(req, res, next) {
    if (req.isAuthenticated()) return next();
    res.status(401).json({ error: 'Not authenticated'});
  }

  //Auth Routes
  app.get('/api/v1/auth/google',
    passport.authenticate('google', { scope: ['profile', 'email']})
  );
  
  app.get('/api/v1/auth/google/callback',
    passport.authenticate('google', { failureRedirect: '/login' }),
    (req, res) => {
      res.redirect(process.env.CLIENT_ORIGIN || 'http://localhost:8080');
    }
  );

  app.get('/api/v1/auth/me', (req, res) => {
    if (!req.isAuthenticated()) return res.status(401).json({ error: 'Not Logged In'});
    const { user_id, user_email, user_name, user_avatar } = req.user;
    res.json({ id: user_id, name: user_name, email: user_email, avatar: user_avatar });
  });

  app.post('/api/v1/auth/logout', (req, res) => {
    req.logout(err => {
      if (err) return res.status(500).json({ error: 'Logout failed'});
      res.json({ ok: true});
    });
  });

  //Favorites Routes
  app.get('/api/favorites', requireAuth, async (req, res) => {
    try {
      const result = await pool.query(
        'SELECT car_id FROM favorites WHERE user_id = $1',
        [req.user.user_id]
      );
      res.json(result.rows.map(r => r.car_id));
    } catch (err) {
      console.error('DB ERROR:', err);
      res.status(500).json({ error: err.message });
    }
  });

  app.post('/api/favorites', requireAuth, async (req, res) => {
    const { car_id } = req.body;
    if (!car_id) return res.status(400).json({ error: 'car_id is required'});
    try {
      await pool.query(
        'INSERT INTO favorites (user_id, car_id) VALUES ($1, $2) ON CONFLICT DO NOTHING',
        [req.user.user_id, car_id]
      );
      res.json({ ok: true });
    } catch (err) {
      console.error('DB ERROR:', err);
      res.status(500).json({ error: err.message });
    }
  });

  app.delete('/api/favorites/:car_id', requireAuth, async (req, res) => {
    try {
      await pool.query(
        'DELETE FROM favorites WHERE user_id = $1 AND car_id = $2',
        [req.user.user_id, req.params.car_id]
      );
      res.json({ ok: true });
    } catch (err) {
      console.error('DB ERROR:', err);
      res.status(500).json({ error: err.message });
    }
  });

  //insert favorites from localStorage on login
  app.post('/api/favorites/sync', requireAuth, async (req, res) => {
    const { car_ids } = req.body;
    if (!Array.isArray(car_ids) || !car_ids.length) return res.json({ ok: true });
    try {
      const values = car_ids.map((_, i) => '($1, $$(i + 2))').join(', ');
      await pool.query(
        `INSERT INTO favorites (user_id, car_id) VALUES ${values} ON CONFLICT DO NOTHING`,
        [req.user.user_id, ...car_ids]
      );
      res.json({ ok: true });
    } catch (err) {
      console.error('DB ERROR:', err);
      res.status(500).json({ error: err.message });
    }
  });

  //Existing routes
    
app.get('/api/cars', async (req, res) => {
  try {
    const result = await pool.query(
      //'SELECT * FROM car'
      `
      SELECT
        c.*,
        ci.image_url,
        j.junkyard_city,
        j.junkyard_state,
        j.junkyard_zip,
        j.junkyard_name
      FROM car c
      LEFT JOIN junkyard j 
        ON c.junkyard_id = j.junkyard_id
      LEFT JOIN (
        SELECT DISTINCT ON (car_id)
          car_id,
          image_url
        FROM car_image 
        ORDER BY car_id, image_id
      ) ci
        ON c.car_id = ci.car_id 
    `);
    
    res.json(result.rows);
    //const [rows] = await pool.query('SELECT * FROM car');
    //res.json(rows);
  } catch (err) {
    console.error('DB ERROR:', err);
    res.status(500).json({ error: err.message });
  }
});

app.get('/api/junkyards', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM junkyard');
    res.json(result.rows);
    //const [rows] = await pool.query('SELECT * FROM junkyard');
    //res.json(rows);
  } catch (err) {
    console.error('DB ERROR:', err);
    res.status(500).json({ error: err.message });
  }
});

app.get('/api/users', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM users');
    res.json(result.rows);
    //const [rows] = await pool.query('SELECT * FROM users');
    //res.json(rows);
  } catch (err) {
    console.error('DB ERROR:', err);
    res.status(500).json({ error: err.message });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, '0.0.0.0', () => console.log(`API running on port ${PORT}`));
