from scrapers.pullnsave import search_pullnsave_inventory
from pipeline.normalize import normalize
from pipeline.ingest import upsert_junkyard, upsert_car, upsert_car_images, mark_all_inactive
from db.connection import get_connection


def main():
    conn = get_connection()
    cur = conn.cursor()

    pullnsave_raw_results = search_pullnsave_inventory()
    raw_data = pullnsave_raw_results.get("data") if isinstance(pullnsave_raw_results, dict) else None
    if not raw_data:
        print("No data returned from pullnsave; skipping ingest.")
        cur.close()
        conn.close()
        return

    # Used to track if cars might have been deleted without actually removing them from the database
    mark_all_inactive(cur)

    for raw in raw_data:
        normalized = normalize(raw, "pullnsave")
        if not normalized:
            continue

        junkyard_id = upsert_junkyard(cur, normalized["junkyard"])
        car_id = upsert_car(cur, normalized["car"], junkyard_id)
        upsert_car_images(cur, car_id, normalized.get("images", []))
    conn.commit()

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
