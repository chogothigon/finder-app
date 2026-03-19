from scrapers.pullnsave import search_pullnsave_inventory
from pipeline.normalize import normalize
from pipeline.ingest import upsert_car, upsert_car_images, upsert_junkyard, mark_all_inactive, load_junkyard_cache
from db.connection import get_connection

'''
def junkyard_key(jy):
    return (
        jy["junkyard_name"],
        jy["junkyard_city"],
        jy["junkyard_state"],
        jy["junkyard_zip"],
        jy["junkyard_website"]
    )


def dedupe_junkyards(normalized_rows):
    junkyard_map = {}
    cars = []

    for row in normalized_rows:
        if not row:
            continue

        jy = row["junkyard"]
        key = junkyard_key(jy)

        # store unique junkyard
        if key not in junkyard_map:
            junkyard_map[key] = jy

        # store car with reference to junkyard key
        cars.append({
            "junkyard_key": key,
            "car": row["car"],
            "images": row.get("images", [])
        })

    return list(junkyard_map.values()), cars'''

def pullnsave(cur, junkyard_cache):
    pullnsave_raw_results = search_pullnsave_inventory()
    for raw in pullnsave_raw_results.get("data"):
        vehicle_info = normalize(raw, "https://www.pullnsave.com")
        if vehicle_info:
            car_id = upsert_car(cur, vehicle_info, junkyard_cache)
            upsert_car_images(cur, car_id, [f"https://app.pullnsaveapp.com/v1/Vehicles/Images/StockId/{raw.get('stockId')}/OrderId/1"])
    print("Finished pullnsave")

def lkq(cur, junkyard_cache):
    pullnsave_raw_results = search_pullnsave_inventory()
    for raw in pullnsave_raw_results.get("data"):
        vehicle_info = normalize(raw, "https://www.pullnsave.com")
        if vehicle_info:
            car_id = upsert_car(cur, vehicle_info, junkyard_cache)
            upsert_car_images(cur, car_id, [f"https://app.pullnsaveapp.com/v1/Vehicles/Images/StockId/{raw.get('stockId')}/OrderId/1"])
    print("Finished pullnsave")

def main():
    '''pullnsave_raw_results = search_pullnsave_inventory()
    vehicle_info = []
    for raw in pullnsave_raw_results.get("data"):
        vehicle_info.append(normalize(raw, "https://www.pullnsave.com"))
    test = dedupe_junkyards(vehicle_info)[0]
    print(test)'''
    
    
    conn = get_connection()
    cur = conn.cursor()
    
    # Used to track if cars might have been deleted without actually removing them from the database 
    mark_all_inactive(cur)

    # Get all junkyard ID's
    junkyard_cache = load_junkyard_cache(cur)
    
    #pullnsave(cur, junkyard_cache)
    lkq(cur, junkyard_cache)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()