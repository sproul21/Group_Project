import requests
from bs4 import BeautifulSoup
import sqlite3
import scrape_functions
import parse_functions


def main(search_term: str):
    db = search_term.replace(' ', '')
    search = search_term.replace(' ', '+')
    create_table = f'CREATE TABLE IF NOT EXISTS {db} (product_name TEXT, rating REAL, num_ratings INTEGER, price ' \
                   f'REAL, product_url TEXT); '

    HEADERS_FOR_GET_REQ = (
        {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/101.0.4951.54 Safari/537.36 ', 'Accept-Language': 'en-US, en;q=0.5'}
    )

    conn = sqlite3.connect('product_data.db')
    cursor = conn.cursor()
    conn.execute(create_table)

    listing_counter = 0
    listing_limit = 300
    url_results_page_param = 1
    while listing_counter < listing_limit:
        results_url_param = f'&page={url_results_page_param}'
        search_page_url = f'{search}{results_url_param}'
        response = requests.get('https://www.amazon.com/s?k=' + search_page_url, headers=HEADERS_FOR_GET_REQ)

        soup_format = BeautifulSoup(response.content, 'html.parser')
        products = soup_format.find_all('div', {'class': 's-result-item', 'data-component-type': 's-search-result'})
        for product in products:

            listing_counter = listing_counter + 1
            if listing_counter > listing_limit:
                break

            product_name = scrape_functions.extract_product_name(product)
            rating = scrape_functions.extract_product_ratings(product)
            num_ratings = scrape_functions.extract_product_num_ratings(product)
            price = scrape_functions.extract_product_price(product)
            product_url = scrape_functions.extract_product_url(product)

            table_insert_string = f'INSERT INTO {db} (product_name, rating, num_ratings, price, product_url) VALUES (' \
                                  f'?, ?, ? ,?,?) '

            cursor.execute(table_insert_string, (product_name, rating, num_ratings, price, product_url))
            conn.commit()

        url_results_page_param = url_results_page_param + 1

    while True:
        user_search = parse_functions.search_params()
        print(user_search)

        choice = input("Would you like to execute another query (yes/no):")
        if choice == "yes":
            continue
        elif choice == "no":
            print("Exiting program...")
            break
        else:
            print("Please enter a valid response (yes/no)")

if __name__ == '__main__':
    search_terms = ['over ear headphones', 'USB microphones', 'Webcams 1080p', 'Capture Cards', 'Eight Channel Audio '
                                                                                                'Mixers',
                    'Gaming Laptops']
    for terms in search_terms:
        main(terms)

