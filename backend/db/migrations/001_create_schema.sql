CREATE TABLE junkyard (
  junkyard_id SERIAL PRIMARY KEY,
  junkyard_city VARCHAR(100) NOT NULL,
  junkyard_state VARCHAR(50) NOT NULL,
  junkyard_zip VARCHAR(10) NOT NULL,
  junkyard_lat NUMERIC(9, 6) NOT NULL,
  junkyard_long NUMERIC(9, 6) NOT NULL,
  junkyard_phone VARCHAR(20) NOT NULL,
  junkyard_website VARCHAR(2048) NOT NULL,
  CONSTRAINT junkyard_unique UNIQUE (junkyard_city, junkyard_state, junkyard_zip, junkyard_website)
);

CREATE TABLE users (
  user_id SERIAL PRIMARY KEY,
  user_email VARCHAR(320) NOT NULL UNIQUE,
  user_googleid VARCHAR(128) NOT NULL UNIQUE
);

CREATE TABLE car (
  car_id SERIAL PRIMARY KEY,
  car_year INT NOT NULL CHECK (car_year BETWEEN 1886 AND YEAR(CURDATE())),
  car_make VARCHAR(50) NOT NULL,
  car_model VARCHAR(50) NOT NULL,
  car_vin VARCHAR(32) NOT NULL,
  car_arrival_date DATE NOT NULL,
  car_engine_data TEXT,
  car_active BOOLEAN NOT NULL DEFAULT TRUE,
  car_source VARCHAR(2048) NOT NULL,
  junkyard_id BIGINT UNSIGNED NOT NULL,
  CONSTRAINT fk_car_junkyard FOREIGN KEY (junkyard_id) REFERENCES junkyard(junkyard_id) ON DELETE RESTRICT,
  CONSTRAINT car_unique UNIQUE (car_vin, junkyard_id, car_arrival_date)
);

CREATE TABLE car_image (
  image_id SERIAL PRIMARY KEY,
  image_url VARCHAR(2048) NOT NULL,
  car_id BIGINT UNSIGNED NOT NULL,
  CONSTRAINT fk_car_image_car FOREIGN KEY (car_id) REFERENCES car(car_id) ON DELETE CASCADE,
  CONSTRAINT car_image_unique UNIQUE (car_id, image_url)
);

CREATE TABLE favorites (
  user_id BIGINT UNSIGNED NOT NULL,
  car_id BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (user_id, car_id),
  CONSTRAINT fk_favorites_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
  CONSTRAINT fk_favorites_car FOREIGN KEY (car_id) REFERENCES car(car_id) ON DELETE CASCADE
);

CREATE INDEX car_junkyard_id_idx ON car(junkyard_id);
CREATE INDEX car_active_idx ON car(car_active);
CREATE INDEX car_arrival_date_idx ON car(car_arrival_date);
CREATE INDEX car_make_model_year_idx ON car(car_make, car_model, car_year);
