import requests
from bs4 import BeautifulSoup

def scrape_pullnsave(make, model, location):
    url = "https://pullnsave.com/wp-admin/admin-ajax.php"

    payload = (
        f"makes={make}&models={model}"
        f"&years=0&endYears=0"
        f"&store={location}"
        f"&beginDate=&endDate=&action=getVehicles"
    )

    headers = {
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "user-agent": "Mozilla/5.0"
    }

    response = requests.post(url, headers=headers, data=payload, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"id": "vehicletable1"})

    if not table:
        return []

    rows = table.find("tbody").find_all("tr")
    results = []

    for row in rows:
        cols = row.find_all("td")

        img = cols[0].find("img")
        image = img["src"] if img else None

        data = [c.text.strip() for c in cols]

        results.append({
            "yard": location,
            "year": int(data[1]),
            "model": data[2],
            "date": data[3],
            "row": data[4],
            "color": data[6],
            "stock_num": data[7],
            "vin": data[8],
            "image": image
        })

    return results
