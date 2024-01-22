import requests
from serpapi import GoogleSearch
import os

from tinydb import TinyDB

def search_pdf_links_for_payment_methods(api_key, payment_methods):
    base_directory = "storage/paymentmethods_terms_conditions_fees"
    if not os.path.exists(base_directory):
        os.makedirs(base_directory, exist_ok=True)

    for i, method in enumerate(payment_methods[:100], start=1):  # Limiting to the first 100 payment methods
        for term in ["terms conditions", "fees"]:
            print(f"Searching for {method} - {term} PDFs...")
            search_params = {
                "engine": "google",
                "q": f"{method['method_name']} {term} filetype:pdf",
                "api_key": api_key,
                "num": "10"  # Adjust based on how many results you'd like to fetch
            }

            search = GoogleSearch(search_params)
            results = search.get_dict()
            pdf_links = [link['link'] for link in results.get('organic_results', []) if link.get('link', '').endswith('.pdf')]

            # Download the first PDF link found for each term
            if pdf_links:
                pdf_url = pdf_links[0]
                filename = os.path.join(base_directory, f"{method['method_name'].replace(' ', '_')}_{term.replace(' ', '_')}.pdf")
                download_pdf(pdf_url, filename)
            else:
                print(f"No PDF found for {method} on {term}.")

def download_pdf(url, filename):
    try:
        # Send a GET request to the URL
        response = requests.get(url, stream=True)
        response.raise_for_status()  # This will raise an exception for HTTP errors

        # Open a file with the specified filename in binary write mode
        with open(filename, 'wb') as f:
            # Write the content of the response to the file in chunks
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Successfully downloaded {filename}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error occurred while downloading {filename}: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while downloading {filename}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while downloading {filename}: {e}")

# Example usage
api_key = "3e538ed895268fb48dbcb6728024903825731c331775a720a75280956fe9adae"
# Initialize TinyDB
db = TinyDB('storage/payment_methods.json')
payment_methods = db.all()

search_pdf_links_for_payment_methods(api_key, payment_methods)