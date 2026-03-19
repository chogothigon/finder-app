import requests
import re

session = requests.Session()

def get_nonce():
    """Visits the inventory page and extracts the 'nonce' from the JS snippet."""
    url = "https://www.pullnsave.com/inventory/"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
    }
    
    response = session.get(url, headers=headers)
    response.raise_for_status()
    
    # Updated regex to match the snippet you found: "nonce": "1125364d02"
    # This looks for the word "nonce", then a colon, then the value inside quotes
    match = re.search(r'"nonce":\s*"([a-f0-9]+)"', response.text)
    
    if match:
        extracted_nonce = match.group(1)
        print(f"Successfully found nonce: {extracted_nonce}")
        return extracted_nonce
    else:
        raise Exception("Could not find the 'nonce' in the page source.")
    

    
def search_pullnsave_inventory(make=0, model=0, yard=0):
    url = "https://www.pullnsave.com/wp-admin/admin-ajax.php"

    current_nonce = get_nonce()

    payload = {
        "action": "pns_get_inventory_assets",
        "search_type": 0,
        "yearStart": 0,
        "yearEnd": 0,
        "make": make,
        "model": model,
        "yard[]": yard,
        "zip": "",
        "radius": 0,
        "security": current_nonce
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
    
    return response.json()  
