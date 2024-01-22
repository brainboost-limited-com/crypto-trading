import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import os

from tinydb import TinyDB

def search_and_download_pdfs(payment_methods):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    for method in payment_methods:
        method_name = method['method_name']
        site = method['url']
        if not site.startswith("http"):
            print(f"Payment method {method_name} requires manual extraction of terms and conditions and fees.")
            continue

        keywords = 'terms conditions fees filetype:pdf'
        search_url = f"https://duckduckgo.com/html/?q=site:{quote_plus(site)}+{quote_plus(keywords)}"
        
        try:
            response = requests.get(search_url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                pdf_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')]
                if pdf_links:
                    for i, pdf_link in enumerate(pdf_links, start=1):
                        download_pdf(pdf_link, f"{method_name}_{i}.pdf", headers)
                else:
                    raise Exception("No PDFs found.")
            else:
                raise Exception("Bad response from server.")
        except Exception as e:
            print(f"Error for {method_name}: {e}. Requires manual extraction.")

def download_pdf(url, filename, headers):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {filename}")
        else:
            raise Exception("Failed to download PDF.")
    except Exception as e:
        print(f"Download error for {filename}: {e}")


# Initialize TinyDB
db = TinyDB('storage/payment_methods.json')
payment_methods = db.all()

search_and_download_pdfs(payment_methods)