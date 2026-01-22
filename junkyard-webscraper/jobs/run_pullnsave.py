from scrapers.pullnsave import scrape_pullnsave
from pipeline.normalize import normalize
from pipeline.ingest import upsert_vehicle
from db.connection import get_connection

def main():
    conn = get_connection()
    cur = conn.cursor()

    raw_results = scrape_pullnsave("Toyota", "Camry", "SLC")

    for raw in raw_results:
        vehicle = normalize(raw, "pullnsave")
        upsert_vehicle(cur, vehicle)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
