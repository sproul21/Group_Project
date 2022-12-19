import sqlite3
import requests
from bs4 import BeautifulSoup


def extract_product_name(product_html_block):
    """This function extracts the product name from the html file and checks if there is a product name"""
    product_name = None
    try:
        product_name = product_html_block.h2.text
    except AttributeError:
        print('no product name')
    finally:
        return product_name


def extract_product_ratings(product_html_block):
    """This function extracts the product rating from the desired product"""
    product_ratings = None
    try:
        #product_ratings = product_html_block.find('i', {'class': 'a-icon'}).text
        product_ratings = product_html_block.find('span', {'aria-label': True}).text
    except AttributeError:
        print('no rating')
    finally:
        return product_ratings


def extract_product_num_ratings(product_html_block):
    """This function extracts the product rating and numbers"""
    product_num_ratings = None
    try:
        product_num_ratings = product_html_block.find('span', {'class': 'a-size-base s-underline-text'}).text
    except AttributeError:
        print('no num ratings')
    finally:
        return product_num_ratings


def extract_product_price(product_html_block):
    """This function extracts the product price"""
    product_price = None
    try:
        price_integer = product_html_block.find('span', {'class': 'a-price-whole'}).text
        price_decimal = product_html_block.find('span', {'class': 'a-price-fraction'}).text
        product_price = price_integer + price_decimal
    except AttributeError:
        print('no price')
    finally:
        return product_price


def extract_product_url(product_html_block):
    """This function extracts our product URL"""
    product_url = None
    try:
        product_url_segment = product_html_block.h2.a['href']
        product_url = 'https://amazon.com' + product_url_segment
    except AttributeError:
        print('no url')
    finally:
        return product_url

def fill_database():
    """This function fills our database, first it searches the terms that we desire
    then creates the table if it doesn't already exist and gives us our desired result"""
    search_terms = ['over ear headphones', 'USB microphones', 'Webcams 1080p', 'Capture Cards', 'Eight Channel Audio '
                                                                                                'Mixers',
                    'Gaming Laptops']
    for terms in search_terms:
        db = terms.replace(' ', '')
        search = terms.replace(' ', '+')
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

                product_name = extract_product_name(product)
                rating = extract_product_ratings(product)
                num_ratings = extract_product_num_ratings(product)
                price = extract_product_price(product)
                product_url = extract_product_url(product)

                table_insert_string = f'INSERT INTO {db} (product_name, rating, num_ratings, price, product_url) VALUES (' \
                                      f'?, ?, ? ,?,?) '

                cursor.execute(table_insert_string, (product_name, rating, num_ratings, price, product_url))
                conn.commit()

            url_results_page_param = url_results_page_param + 1
