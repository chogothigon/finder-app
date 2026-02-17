INSERT INTO junkyard (
  junkyard_city,
  junkyard_state,
  junkyard_zip,
  junkyard_lat,
  junkyard_long,
  junkyard_phone,
  junkyard_website
) VALUES
  ('Salt Lake City', 'UT', '84101', 40.760780, -111.891045, '801-555-0100', 'https://example-junkyard.com');

INSERT INTO users (user_email, user_googleid) VALUES
  ('user1@example.com', 'google-oauth-123');

INSERT INTO car (
  car_year,
  car_make,
  car_model,
  car_vin,
  car_arrival_date,
  car_engine_data,
  car_active,
  car_source,
  junkyard_id
) VALUES
  (2012, 'HONDA', 'CIVIC', '2HGFB2F59CH000001', '2026-02-01', '1.8L I4', TRUE, 'https://example-junkyard.com/listings/1', 1);

INSERT INTO car_image (image_url, car_id) VALUES
  ('https://example-junkyard.com/images/1.jpg', 1);

INSERT INTO favorites (user_id, car_id) VALUES
  (1, 1);
