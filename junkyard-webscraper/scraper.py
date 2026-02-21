from scrapers.pullnsave import search_pullnsave_inventory
from pipeline.normalize import normalize
from pipeline.ingest import upsert_vehicle, mark_all_inactive
from db.connection import get_connection


def main():
    #conn = get_connection()
    #cur = conn.cursor()
    
    # Used to track if cars might have been deleted without actually removing them from the database 
    #mark_all_inactive(cur)

    pullnsave_raw_results = search_pullnsave_inventory() #maybe just change so it doesn't use 0 later?
    for raw in pullnsave_raw_results.get("data"):
        vehicle = normalize(raw, "pullnsave")
        if vehicle:
            upsert_vehicle(cur, vehicle)
    conn.commit()

    



    
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
