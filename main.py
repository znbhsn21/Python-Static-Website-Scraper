import requests
from bs4 import BeautifulSoup
import csv
import time

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

all_data = []

for page_num in range(1, 3):  
    print(f"Fetching Page {page_num}...")
    url = BASE_URL.format(page_num)
    
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Skipping page {page_num}: Status {response.status_code}")
            continue
            
        soup = BeautifulSoup(response.text, 'lxml')
        items = soup.find_all('article', class_='product_pod')

        for item in items:

            title_tag = item.h3.find('a')
            title = title_tag['title'].strip() if title_tag else "Unknown Title"
            
            price_tag = item.find('p', class_='price_color')
            price = price_tag.text.strip() if price_tag else "N/A"
            
            stock_tag = item.find('p', class_='instock availability')
            stock = stock_tag.text.strip() if stock_tag else "Unknown"

            all_data.append({
                "Title": title,
                "Price": price,
                "Availability": stock
            })

        time.sleep(1)

    except Exception as e:
        print(f"An error occurred: {e}")

filename = "scraped_data.csv"
if all_data:
    keys = all_data[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(all_data)
    
    print("-" * 30)
    print(f"Success! Scraped {len(all_data)} items.")
    print(f"File saved as: {filename}")
