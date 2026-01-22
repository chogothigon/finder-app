def normalize(raw, source_site):
    return {
        "source_site": source_site,
        "yard_name": raw.get("yard"),
        "yard_location": "UT",
        "stock_number": raw.get("stock_num"),
        "vin": raw.get("vin"),
        "year": raw.get("year"),
        "make": None,
        "model": raw.get("model"),
        "color": raw.get("color"),
        "row_location": raw.get("row"),
        "arrival_date": raw.get("date"),
        "image_url": raw.get("image"),
    }
