import requests
from bs4 import BeautifulSoup

def get_makes_from_pullnsave():
    url = "https://pullnsave.com/wp-admin/admin-ajax.php"

    payload = {
        "action": "getMakes"
    }

    headers = {
        "accept": "*/*",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://www.pullnsave.com",
        "referer": "https://www.pullnsave.com/",
        "x-requested-with": "XMLHttpRequest",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/144.0.0.0 Safari/537.36"
        )
    }

    response = requests.post(url, data=payload, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    makes = []
    for option in soup.find_all("option"):
        value = option.get("value")
        text = option.get_text(strip=True)

        if value:
            makes.append(text)

    return makes

def search_pullnsave_inventory(make, model=0, yard=0):
    url = "https://www.pullnsave.com/wp-admin/admin-ajax.php"

    payload = {
        "action": "pns_get_inventory_assets",
        "search_type": 0,
        "yearStart": 0,
        "yearEnd": 0,
        "make": make, # make.upper() used to be
        "model": model,
        "yard[]": yard,
        "zip": "",
        "radius": 0,
        "security": "0418e80fd5"  # ⚠️ dynamic nonce
    }

    headers = {
        "accept": "*/*",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "x-requested-with": "XMLHttpRequest",
        "origin": "https://www.pullnsave.com",
        "referer": "https://www.pullnsave.com/inventory/",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/144.0.0.0 Safari/537.36"
        )
    }

    response = requests.post(url, data=payload, headers=headers)
    response.raise_for_status()

    data = response.json()

    if not data.get("success"):
        return []
    '''
    results = []

    for car in data["data"]:
        car_data = {
            "yard": car["yardName"],
            "year": car["year"],
            "make": car["make"],
            "model": car["model"],
            "color": car["color"],
            "vin": car["vin"],
            "stock_num": car["stockId"],
            "row": car["yardRow"],
            "date": car["rcvdDtTm"],
            "yard_address": car["yardAddress"],
            "yard_zip": car["yardZip"]
        }
        results.append(car_data)
    '''
    return data
