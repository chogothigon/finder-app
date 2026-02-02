def mark_all_inactive(cur, source_site):
    cur.execute("""
        UPDATE vehicles
        SET is_active = FALSE;
    """)

def upsert_vehicle(cur, v):
    cur.execute("""
        INSERT INTO vehicles (
            source_site, stock_number, vin,
            make, model, year, color,
            yard_name, yard_location,
            yard_zip, yard_row,
            first_seen, last_seen, is_active
        )
        VALUES (
            %(source_site)s, %(stock_number)s, %(vin)s,
            %(make)s, %(model)s, %(year)s, %(color)s,
            %(yard_name)s, %(yard_location)s,
            %(yard_zip)s, %(yard_row)s,
            NOW(), NOW(), TRUE
        )
        ON CONFLICT (source_site, stock_number)
        DO UPDATE SET
            vin = EXCLUDED.vin,
            make = EXCLUDED.make,
            model = EXCLUDED.model,
            year = EXCLUDED.year,
            color = EXCLUDED.color,
            yard_name = EXCLUDED.yard_name, 
            yard_location = EXCLUDED.yard_location,
            yard_zip = EXCLUDED.yard_zip,
            yard_row = EXCLUDED.yard_row,
            last_seen = NOW(),
            is_active = TRUE;
    """, v)