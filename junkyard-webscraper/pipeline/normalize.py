from datetime import datetime, date


def _truncate(value, max_len):
    if value is None:
        return None
    value = str(value).strip()
    return value[:max_len]


def _parse_city_state_zip(address, fallback_zip):
    if not address:
        return "Unknown", "Unknown", _truncate(fallback_zip or "00000", 10)

    parts = [part.strip() for part in address.split(",") if part.strip()]
    city = "Unknown"
    state = "Unknown"
    zip_code = _truncate(fallback_zip or "00000", 10)

    if len(parts) >= 2:
        city = parts[-2]
        state_zip = parts[-1].split()
        if state_zip:
            state = state_zip[0]
        if len(state_zip) > 1 and not fallback_zip:
            zip_code = _truncate(state_zip[1], 10)

    return city, state, zip_code


def _parse_arrival_date(raw_date):
    if not raw_date:
        return date.today().isoformat()
    try:
        return datetime.fromisoformat(str(raw_date)).date().isoformat()
    except ValueError:
        return date.today().isoformat()


def normalize(raw, source_site):
    if not raw.get("stockId"):
        print("Skipping vehicle, missing stock_number:", raw)
        return None

    if not raw.get("year") or not raw.get("make") or not raw.get("model"):
        print("Skipping vehicle, missing required fields:", raw)
        return None

    yard_address = raw.get("yardAddress")
    yard_zip = raw.get("yardZip")
    city, state, zip_code = _parse_city_state_zip(yard_address, yard_zip)

    return {
        "junkyard": {
            "junkyard_city": _truncate(city, 100) or "Unknown",
            "junkyard_state": _truncate(state, 50) or "Unknown",
            "junkyard_zip": _truncate(zip_code, 10) or "00000",
            "junkyard_lat": 0.0,
            "junkyard_long": 0.0,
            "junkyard_phone": "N/A",
            "junkyard_website": "https://www.pullnsave.com"
        },
        "car": {
            "car_year": int(raw.get("year")),
            "car_make": _truncate(raw.get("make", "").upper(), 50),
            "car_model": _truncate(raw.get("model", "").upper(), 50),
            "car_vin": _truncate(raw.get("vin") or raw.get("stockId"), 32),
            "car_arrival_date": _parse_arrival_date(raw.get("rcvdDtTm")),
            "car_engine_data": _truncate(raw.get("engine") or "", 1024),
            "car_active": True,
            "car_source": "https://www.pullnsave.com/inventory/"
        },
        "images": raw.get("image_urls", [])
    }
