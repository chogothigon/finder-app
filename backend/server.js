const express = require('express');
const cors = require('cors');
//const mysql = require('mysql2/promise');
const { Pool } = require('pg');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

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

app.get('/api/cars', async (req, res) => {
  try {
    const result = await pool.query(
      //'SELECT * FROM car'
      SELECT
        c.*,
        ci.image_url
      FROM car c
      LEFT JOIN (
        SELECT DISTINCT ON (car_id)
        car_id,
        image_url
      FROM car_image 
      ORDER BY car_id, image_id
  ) ci
    ON c.car_id = ci.car_id 
    );
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
