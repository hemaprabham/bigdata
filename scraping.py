import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_product_details(product_urls):
    product_details = []

    for url in product_urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        product_description = soup.find('div', {'id': 'productDescription'})
        description = product_description.get_text().strip() if product_description else None

        product_asin = soup.find('th', text='ASIN')
        asin = product_asin.find_next('td').get_text().strip() if product_asin else None

        product_manufacturer = soup.find('a', {'id': 'bylineInfo'})
        manufacturer = product_manufacturer.get_text().strip() if product_manufacturer else None

        product_info = {
            'Product URL': url,
            'Description': description,
            'ASIN': asin,
            'Product Description': product_description,
            'Manufacturer': manufacturer
        }

        product_details.append(product_info)

        time.sleep(1)  # Add a delay of 1 second to be respectful of the server

    return product_details

if __name__ == '__main__':
    base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1'
    num_pages_to_scrape = 20

    # Scraping product URLs from the initial listing pages
    product_urls = []
    for page in range(1, num_pages_to_scrape + 1):
        page_url = base_url + f"&page={page}"
        response = requests.get(page_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        product_containers = soup.find_all('div', {'data-component-type': 's-search-result'})
        for product in product_containers:
            product_url = 'https://www.amazon.in' + product.find('a', {'class': 'a-link-normal'})['href']
            product_urls.append(product_url)

    # Scraping product details from the product URLs
    product_details = scrape_product_details(product_urls[:200])  # Limiting to 200 URLs as requested

    # Exporting the data to a CSV file
    csv_file = 'amazon_product_details.csv'
    fieldnames = ['Product URL', 'Description', 'ASIN', 'Product Description', 'Manufacturer']
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for product in product_details:
            writer.writerow(product)

    print(f"Scraping and CSV export completed successfully to {csv_file}.")
