def mark_all_inactive(cur):
    cur.execute("""
        UPDATE car
        SET car_active = FALSE;
    """)


def upsert_junkyard(cur, junkyard):
    cur.execute("""
        INSERT INTO junkyard (
            junkyard_city,
            junkyard_state,
            junkyard_zip,
            junkyard_lat,
            junkyard_long,
            junkyard_phone,
            junkyard_website
        )
        VALUES (
            %(junkyard_city)s,
            %(junkyard_state)s,
            %(junkyard_zip)s,
            %(junkyard_lat)s,
            %(junkyard_long)s,
            %(junkyard_phone)s,
            %(junkyard_website)s
        )
        ON CONFLICT (junkyard_city, junkyard_state, junkyard_zip, junkyard_website)
        DO UPDATE SET
            junkyard_phone = EXCLUDED.junkyard_phone,
            junkyard_lat = EXCLUDED.junkyard_lat,
            junkyard_long = EXCLUDED.junkyard_long
        RETURNING junkyard_id;
    """, junkyard)
    return cur.fetchone()[0]


def upsert_car(cur, car, junkyard_id):
    payload = {**car, "junkyard_id": junkyard_id}
    cur.execute("""
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
        )
        VALUES (
            %(car_year)s,
            %(car_make)s,
            %(car_model)s,
            %(car_vin)s,
            %(car_arrival_date)s,
            %(car_engine_data)s,
            %(car_active)s,
            %(car_source)s,
            %(junkyard_id)s
        )
        ON CONFLICT (car_vin, junkyard_id, car_arrival_date)
        DO UPDATE SET
            car_make = EXCLUDED.car_make,
            car_model = EXCLUDED.car_model,
            car_year = EXCLUDED.car_year,
            car_engine_data = EXCLUDED.car_engine_data,
            car_active = TRUE,
            car_source = EXCLUDED.car_source
        RETURNING car_id;
    """, payload)
    return cur.fetchone()[0]


def upsert_car_images(cur, car_id, image_urls):
    for url in image_urls:
        cur.execute("""
            INSERT INTO car_image (image_url, car_id)
            VALUES (%s, %s)
            ON CONFLICT (car_id, image_url) DO NOTHING;
        """, (url, car_id))