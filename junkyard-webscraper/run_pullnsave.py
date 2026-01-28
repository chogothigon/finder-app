from scrapers.pullnsave import get_makes_from_pullnsave,search_pullnsave_inventory
from pipeline.normalize import normalize
from pipeline.ingest import upsert_vehicle, mark_all_inactive
from db.connection import get_connection

def main():
    conn = get_connection()
    cur = conn.cursor()

    # makes = get_makes_from_pullnsave()
    # del makes[0]
    
    # This can probably be simplified into just a simple 0 querry for make
    '''
    car_data = []
    for make in makes:
        car_data.append(search_pullnsave_inventory(make))
    '''
    raw_results = search_pullnsave_inventory(0)
    mark_all_inactive(cur, "pullnsave") # Change these static variables later
    for raw in raw_results.get("data"):
        vehicle = normalize(raw, "pullnsave")
        if vehicle:
            upsert_vehicle(cur, vehicle)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
