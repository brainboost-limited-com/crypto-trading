import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
import validators
import os
from tinydb import TinyDB
from tinydb.storages import JSONStorage

# Directory where the database will be stored
db_directory = "storage"
db_file = "payment_methods.json"

# Ensure the directory exists
os.makedirs(db_directory, exist_ok=True)

# Initialize TinyDB
db = TinyDB(os.path.join(db_directory, db_file), storage=JSONStorage)

def sanitize_method_name(method_name):
    # Remove invalid characters and replace spaces with hyphens
    sanitized_name = re.sub(r'[^\w\s-]', '', method_name).replace(' ', '-').lower()
    return sanitized_name

def validate_and_correct_url(url):
    while not validators.url(url):
        # Remove characters until the URL is valid
        url = url.rsplit('-', 1)[0]
        if not url:
            break
    return url

def search_duckduckgo(query):
    url = f"https://html.duckduckgo.com/html?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    for link in soup.find_all('a', {'class': 'result__a'}):
        extracted_url = link.get('href')
        if extracted_url:
            # Extract actual URL from DuckDuckGo redirect URL
            parsed_url = urlparse(extracted_url, 'http')
            url_params = {kv.split('=')[0]: kv.split('=')[1] for kv in parsed_url.query.split('&') if kv}
            target_url = url_params.get('uddg')

            if target_url:
                domain = urlparse(target_url).netloc
                sanitized_query = sanitize_method_name(query)
                # Check if the domain matches the expected format
                if sanitized_query in domain:
                    valid_url = validate_and_correct_url(target_url)
                    return valid_url

    return None

payment_methods = [
    "Skrill",
    "Zelle",
    "Banco Pichincha",
    "Zinli",
    "AirTM",
    "Bank Transfer",
    "Perfect Money",
    "Banco Guayaquil",
    "Banesco Panama",
    "Payeer",
    "Produbanco",
    "Neteller",
    "Bank of America",
    "Credit Bank of Peru",
    "Pyypl",
    "Banco de Credito",
    "Interbank",
    "Banco del Pacifico",
    "Banco General Panama",
    "Facebank International",
    "ABA",
    "Mercantil Bank Panama",
    "Bank of Georgia",
    "Wally Tech",
    "Banco Bolivariano",
    "Cash app",
    "Prex",
    "BBVA",
    "TBC Bank",
    "Mony",
    "Banistmo Panama",
    "Scotiabank Peru",
    "International Wire",
    "Bank Transfer",
    "BAC Costa Rica",
    "Western Union",
    "Towerbank",
    "ZEN",
    "Bank Transfer",
    "ACLEDA",
    "Banco de Costa Rica",
    "Wing Money",
    "Itaú Uruguay",
    "MoMo",
    "Transferencia Bancaria Costa Rica",
    "KHQR",
    "Dukascopy Bank",
    "Utoppia",
    "Cash Deposit to Bank",
    "Pipol Pay",
    "Ameriabank",
    "BAC Credomatic",
    "Bank Transfer",
    "Alipay",
    "GrabrFi",
    "Banco Brubank",
    "Banco Santander Uruguay",
    "Bank of the Republic of Uruguay",
    "Moneygram",
    "Paysend.com",
    "Transferencia ACH",
    "Banco BAC Credomatic SV",
    "Naranja X",
    "Banco Agricola SV",
    "Bank Transfer",
    "Pago Movil",
    "Scotiabank Costa Rica",
    "First Bank Of Nigeria",
    "OCA Blue",
    "ZaloPay",
    "Ziraat",
    "Banco Promerica SV",
    "Abu Dhabi Commercial Bank ADCB",
    "Banco Santander Argentina",
    "ADIB: Abu Dhabi Islamic Bank",
    "Whish MONEY",
    "Bank Transfer",
    "Emirates NBD",
    "Viettel Money",
    "Papara",
    "Reba",
    "Venmo",
    "Global66",
    "Scotiabank Uruguay",
    "Banco Davivienda SV",
    "Denizbank",
    "Nequi",
    "VakifBank",
    "Instant Transfer",
    "N26",
    "BBVA Uruguay",
    "Bank of the Philippine Islands",
    "Banco Hipotecario SV",
    "Maybank",
    "Payme.io",
    "Uphold",
    "Scotiabank Panama",
    "WeChat",
    "Banco De Oro",
    "Gcash",
    "Red Pagos",
    "Starling Bank",
    "Apelsin",
    "Davivienda S.A",
    "Maya",
    "Banco Popular",
    "Česká spořitelna",
    "ShopeePay-SEA",
    "Bank Transfer",
    "Easypaisa-PK Only",
    "Meezan Bank",
    "DSK Bank",
    "Garanti",
    "Kuveyt Turk",
    "Multibank Panama",
    "Paynet",
    "Arab Bank",
    "BAC Credomatic Nicaragua",
    "BCR Bank",
    "Metropolitan Bank of the Philippines",
    "PayPro"
]

payment_method_objects = []

for method in payment_methods:
    sanitized_method = sanitize_method_name(method)
    url = search_duckduckgo(sanitized_method)
    if not url:
        guess_url = f"https://{sanitized_method}.com"
        url = validate_and_correct_url(guess_url)
    payment_method_objects.append({'method_name': method, 'url': url})

# Insert payment methods into the database
db.insert_multiple(payment_method_objects)

print(f"{len(payment_method_objects)} payment methods have been inserted into the database.")


# Example output
print(payment_method_objects[:3])  # Print first 3 for example