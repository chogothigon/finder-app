-- REST API support views for the final page list:
-- search, user favorites, random car, car info + images, and login.

DROP VIEW IF EXISTS vw_random_car_pool;
DROP VIEW IF EXISTS vw_search_filter_options;
DROP VIEW IF EXISTS vw_search_results;
DROP VIEW IF EXISTS vw_user_favorites;
DROP VIEW IF EXISTS vw_car_info;
DROP VIEW IF EXISTS vw_car_images;
DROP VIEW IF EXISTS vw_login_users;

-- Legacy view cleanup from earlier lab drafts.
DROP VIEW IF EXISTS vw_random_pool;
DROP VIEW IF EXISTS vw_car_search_results;
DROP VIEW IF EXISTS vw_about_metrics;
DROP VIEW IF EXISTS vw_donate_contacts;
DROP VIEW IF EXISTS vw_car_form;
DROP VIEW IF EXISTS vw_junkyard_form;
DROP VIEW IF EXISTS vw_user_form;
DROP VIEW IF EXISTS vw_favorites_form;
DROP VIEW IF EXISTS vw_car_image_form;

CREATE VIEW vw_search_results AS
SELECT
  c.car_id,
  c.car_year,
  c.car_make,
  c.car_model,
  CONCAT(c.car_year, ' ', c.car_make, ' ', c.car_model) AS car_display_name,
  c.car_arrival_date,
  c.car_engine_data,
  c.car_active,
  c.car_source,
  ci.image_url AS primary_image_url,
  j.junkyard_id,
  j.junkyard_city,
  j.junkyard_state,
  j.junkyard_zip,
  j.junkyard_phone,
  j.junkyard_website
FROM car c
JOIN junkyard j ON j.junkyard_id = c.junkyard_id
LEFT JOIN car_image ci ON ci.image_id = (
  SELECT MIN(ci2.image_id)
  FROM car_image ci2
  WHERE ci2.car_id = c.car_id
)
WHERE c.car_active = TRUE;

CREATE VIEW vw_search_filter_options AS
SELECT DISTINCT
  c.car_make,
  c.car_model,
  c.car_year,
  j.junkyard_city,
  j.junkyard_state
FROM car c
JOIN junkyard j ON j.junkyard_id = c.junkyard_id
WHERE c.car_active = TRUE;

-- Endpoint usage: SELECT * FROM vw_random_car_pool ORDER BY RAND() LIMIT 1;
CREATE VIEW vw_random_car_pool AS
SELECT *
FROM vw_search_results;

CREATE VIEW vw_user_favorites AS
SELECT
  u.user_id,
  u.user_email,
  u.user_googleid,
  f.car_id,
  c.car_year,
  c.car_make,
  c.car_model,
  CONCAT(c.car_year, ' ', c.car_make, ' ', c.car_model) AS car_display_name,
  c.car_arrival_date,
  c.car_active,
  c.car_source,
  ci.image_url AS primary_image_url,
  j.junkyard_id,
  j.junkyard_city,
  j.junkyard_state,
  j.junkyard_zip,
  j.junkyard_phone,
  j.junkyard_website
FROM favorites f
JOIN users u ON u.user_id = f.user_id
JOIN car c ON c.car_id = f.car_id
JOIN junkyard j ON j.junkyard_id = c.junkyard_id
LEFT JOIN car_image ci ON ci.image_id = (
  SELECT MIN(ci2.image_id)
  FROM car_image ci2
  WHERE ci2.car_id = c.car_id
);

CREATE VIEW vw_car_info AS
SELECT
  c.car_id,
  c.car_year,
  c.car_make,
  c.car_model,
  CONCAT(c.car_year, ' ', c.car_make, ' ', c.car_model) AS car_display_name,
  c.car_vin,
  c.car_arrival_date,
  c.car_engine_data,
  c.car_active,
  c.car_source,
  ci.image_url AS primary_image_url,
  j.junkyard_id,
  j.junkyard_city,
  j.junkyard_state,
  j.junkyard_zip,
  j.junkyard_lat,
  j.junkyard_long,
  j.junkyard_phone,
  j.junkyard_website,
  (SELECT COUNT(*) FROM car_image ci_count WHERE ci_count.car_id = c.car_id) AS image_count,
  (SELECT COUNT(*) FROM favorites f_count WHERE f_count.car_id = c.car_id) AS favorite_count
FROM car c
JOIN junkyard j ON j.junkyard_id = c.junkyard_id
LEFT JOIN car_image ci ON ci.image_id = (
  SELECT MIN(ci2.image_id)
  FROM car_image ci2
  WHERE ci2.car_id = c.car_id
);

CREATE VIEW vw_car_images AS
SELECT
  ci.image_id,
  ci.car_id,
  ci.image_url,
  CONCAT(c.car_year, ' ', c.car_make, ' ', c.car_model) AS car_display_name
FROM car_image ci
JOIN car c ON c.car_id = ci.car_id;

CREATE VIEW vw_login_users AS
SELECT
  u.user_id,
  u.user_email,
  u.user_googleid
FROM users u;
