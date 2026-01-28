def normalize(raw, source_site):
    if not raw.get("stockId"):
        print("Skipping vehicle, missing stock_number:", raw)
    else: 
        return {
            "source_site": source_site,
            "stock_number": raw.get("stockId"),
            "vin": raw.get("vin"),
            "make": raw.get("make"),
            "model": raw.get("model"),
            "year": raw.get("year"),
            "color": raw.get("color"),
            "yard_name": raw.get("yardName"),
            "yard_location": raw.get("yardAddress"),
            "yard_zip": raw.get("yardZip"),
            "yard_row": raw.get("yardRow")
        }
