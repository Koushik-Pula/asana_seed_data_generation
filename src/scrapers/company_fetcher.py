import requests
from bs4 import BeautifulSoup
import logging
import random

logger = logging.getLogger(__name__)

def fetch_real_company_names(limit=5):
    url = "https://en.wikipedia.org/wiki/List_of_S&P_500_companies"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        logger.info(f"Scraping company names from {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        table = soup.find('table', {'id': 'constituents'})
        if not table:
            logger.warning("Could not find the table. Using fallback names.")
            return _fallback_names()
            
        companies = []
        for row in table.find_all('tr')[1:]:
            cols = row.find_all('td')
            if cols:
                name = cols[1].get_text(strip=True)
                companies.append(name)
        
        random.shuffle(companies)
        return companies[:limit]

    except Exception as e:
        logger.warning(f"Scraping failed: {e}. Switching to fallback data.")
        return _fallback_names()

def _fallback_names():
    return ["Acme Corp", "Globex Corporation", "Soylent Corp", "Initech", "Umbrella Corp", "Stark Industries", "Wayne Enterprises"]