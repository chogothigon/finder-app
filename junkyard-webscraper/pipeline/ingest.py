def upsert_vehicle(cur, v):
    cur.execute("""
        INSERT INTO vehicles (
            source_site, yard_name, yard_location,
            stock_number, vin,
            year, make, model, color,
            row_location, arrival_date, image_url
        )
        VALUES (
            %(source_site)s, %(yard_name)s, %(yard_location)s,
            %(stock_number)s, %(vin)s,
            %(year)s, %(make)s, %(model)s, %(color)s,
            %(row_location)s, %(arrival_date)s, %(image_url)s
        )
        ON CONFLICT (source_site, stock_number)
        DO UPDATE SET
            vin = EXCLUDED.vin,
            year = EXCLUDED.year,
            model = EXCLUDED.model,
            color = EXCLUDED.color,
            row_location = EXCLUDED.row_location,
            arrival_date = EXCLUDED.arrival_date,
            image_url = EXCLUDED.image_url,
            scraped_at = NOW();
    """, v)
