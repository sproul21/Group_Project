"""
    This module contains functions that scrape product data from Amazon's product listing pages; it consists of two
    functions:

    'get_single_listing_product_name()'
    --> issues a GET request to a hard coded target URL
        ('https://www.amazon.com/dp/B08J5F3G18/'). This URL maps to the Amazon product page for a high-end graphics
        card. The product title string is extracted from the web response content (HTML) and printed to a text file
        and to the terminal.

    'get_multiple_listings_by_keyword(keywords: str)'
    --> This function conducts an Amazon product search using the search keywords passed in as this function's
        only parameter. Product data is extracted from the first page of search results. This data is printed to a
        text file and to the terminal.

    ** This module is a DEMO; it lacks proper error checking and does not exhibit "clean code" characteristics. **
"""
import sqlite3
from sqlite3 import Error
import requests
from bs4 import BeautifulSoup

# Author: Joseph Matta (December 2022)
__author__ = 'Joseph Matta'
__copyright__ = 'Copyright December 2022, Amazon Scaper DEMO'
__version__ = '1.0'
__email__ = 'j1matta@bridgew.edu'

# Attach this header to all GET requests sent to Amazon servers.
# You can find out your unique 'User Agent' string by visiting the following website:
# https://dnschecker.org/user-agent-info.php
HEADERS_FOR_GET_REQ = (
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/101.0.4951.54 Safari/537.36 ', 'Accept-Language': 'en-US, en;q=0.5'}
)


def get_multiple_listings_by_keyword(keywords: str):
    """ This function first conducts an Amazon keyword search using the search keywords passed in as this function's
        only parameter. Product data is extracted from the first page of search results.
        The following data points are extracted from each product listing shown on the first page of search results:

        1. Product Title
        2. Product Star Rating
        3. Number of Ratings
        4. Product Selling Price
        5. Product URL (encoded in the product title)

        This data is printed to the terminal and to a text file. """

    # make/open a text file to store the product name
    data_out_file = open("output_data.txt", "w")

    # replace spaces in the 'keywords' parameter string with '+' to insert into the request url.
    # Typical of many URL formats, space characters (' ') are represented by '+'.
    query_terms = keywords.replace(' ', '+')
    # this is the base "search on keyword" Amazon URL:
    base_amazon_search_url = 'https://www.amazon.com/s?k='
    # construct the URL by incorporating the search keywords
    search_url = f'{base_amazon_search_url}{query_terms}'

    # Add a 'page' parameter to the URL.
    # (Amazon URLs use '&' to separate URL parameters.)
    search_url += '&page=1'  # Note: this will only get the first page of search results (page=1).
    # issue GET request with the USER AGENT header
    response = requests.get(search_url, headers=HEADERS_FOR_GET_REQ)
    print('\n' + '>> search URL: ' + search_url + '\n')
    data_out_file.write(f'\n{search_url}\n\n')

    # The 'response' object contains all the target URL's HTML code in its '.content' property.
    # The BeautifulSoup class helps with parsing the HTML text.
    soup_format = BeautifulSoup(response.content, 'html.parser')

    # Gather only the search results we are looking for - use the 'Inspect' tool to highlight the items we are
    # interested in...
    # ... some search results are not the "main" search results - these can include advertisements or "sponsored"
    # products.
    # After highlighting using the 'Inspect' tool, we found that product listings are discovered in the following way:
    # search for <div> tags - inside <div> tags look for 's-result-item'... but not all 's-result-item' classes
    # are what we are looking for. Now look at the 'data-component-type' attribute, find those that have the value
    # 's-search-result' - these are the result listing HTML blocks we are looking for.
    # The '.find_all()' function will return a BS class approximating a Python list. This list structure is NOT
    # a Python list type, but it has similar capabilities and behaviors. For example, you may iterate through and
    # index the elements of the 'search_results' BS object just as you would with a Python list.
    # Essentially, this list is a collection of HTML blocks that code for each product listing displayed on the
    # results page.
    search_results = soup_format.find_all('div', {'class': 's-result-item', 'data-component-type': 's-search-result'})

    # iterate through the result listing HTML blocks:
    for listing_block in search_results:
        # (finding what tags to target for each listing page element can be done by right-clicking on the website
        # component and "inspecting" the HTML code for that attribute)

        # get product name from listing - these are inside an <h2> tag.
        # using the BS class capabilities, we can access the 'text' portion of an HTML block using the BS '.text'
        # property.
        product_name = listing_block.h2.text
        print(product_name)
        data_out_file.write(f'{product_name}\n')

        # * get product ratings *
        # - upon inspection, the rating elements are contained in <i> tag blocks
        # we need a try/except structure because not all items may have a rating...
        try:
            # relevant page elements were found by inspecting the element of interest
            # extract star rating
            rating_info = listing_block.find('i', {'class': 'a-icon'}).text
            print(rating_info)
            data_out_file.write(f'{rating_info}\n')
            # extract number of ratings
            num_ratings = listing_block.find('span', {'class': 'a-size-base s-underline-text'}).text
            print(num_ratings)
            data_out_file.write(f'{num_ratings}\n')
        # An AttributeError exception will be thrown if the '.find()' function does not find an HTML block with the
        # supplied parameters.
        except AttributeError:
            # If no star ratings are reported for the current product listing, inform the user with print statements
            # to terminal and text file.
            print('No Ratings')
            data_out_file.write('No Ratings\n')

        # * get product price *
        # Product price elements have two components - the whole dollar amount (integer)
        # and the cents (decimal) component.
        # Use a try/except block just in case the product does not have a price listed.
        try:
            price_integer = listing_block.find('span', {'class': 'a-price-whole'}).text
            price_decimal = listing_block.find('span', {'class': 'a-price-fraction'}).text
            print(price_integer + price_decimal)
            data_out_file.write(price_integer + price_decimal + '\n')
        except AttributeError:
            # if listing does not have a price, inform the user
            print('No Price')
            data_out_file.write('No Price\n')

        # * get product URL *
        # use try/except in case product does not have a direct URL (unlikely)
        try:
            # Navigable URLs (links) are typically stored in the HTML 'href' attribute.
            # We can use the BS tools and access functionalities to extract the product URL. The URL string is
            # an attribute of the product title. This makes sense because the product title element doubles as
            # a hyperlink to the product's dedicated page.
            product_url_segment = listing_block.h2.a['href']
            # Because the 'href' string is only the unique portion of the product URL, we must add the Amazon
            # URL prefix (base) portion to get a complete URL.
            complete_product_url = 'https://amazon.com' + product_url_segment
            print(complete_product_url)
            data_out_file.write(complete_product_url + '\n')
        except AttributeError:
            print('No Product URL')
            data_out_file.write('No Product URL\n')

        # print blank line between individual product data
        print()
        data_out_file.write('\n\n')

def create_db():
    db_connection = None

    try:
        db_name = 'products.db'

        db_connection = sqlite3.connect(db_name)

        db_cursor = db_connection.cursor()

        db_cursor.execute('''CREATE TABLE IF NOT EXISTS 'Over Ear Headphones' (
                                        product_name TEXT,
                                         rating REAL,
                                         num_ratings INTEGER,
                                         price REAL,
                                         product_url TEXT
                                     ); ''')
        db_cursor.execute('''CREATE TABLE IF NOT EXISTS 'USB Microphones' (
                                        product_name TEXT,
                                         rating REAL,
                                         num_ratings INTEGER,
                                         price REAL,
                                         product_url TEXT
                                     ); ''')
        db_cursor.execute('''CREATE TABLE IF NOT EXISTS '1080p Webcams' (
                                                 product_name TEXT,
                                                 rating REAL,
                                                 num_ratings INTEGER,
                                                 price REAL,
                                                 product_url TEXT
                                             ); ''')
        db_cursor.execute('''CREATE TABLE IF NOT EXISTS 'Capture Cards' (
                                                 product_name TEXT,
                                                 rating REAL,
                                                 num_ratings INTEGER,
                                                 price REAL,
                                                 product_url TEXT
                                             ); ''')
        db_cursor.execute('''CREATE TABLE IF NOT EXISTS '8-channel Audio Mixers' (
                                                 product_name TEXT,
                                                 rating REAL,
                                                 num_ratings INTEGER,
                                                 price REAL,
                                                 product_url TEXT
                                             ); ''')
        db_cursor.execute('''CREATE TABLE IF NOT EXISTS 'Gaming Laptops' (
                                                 product_name TEXT,
                                                 rating REAL,
                                                 num_ratings INTEGER,
                                                 price REAL,
                                                 product_url TEXT
                                             ); ''')

    except Error as e:
        print(e)

if __name__ == '__main__':
    # prompt to have the user supply product search keywords
    user_input_search_keywords = input('\n>> Enter product keywords to search in Amazon\'s e-marketplace:\n>> ')
    # pass the user-supplied keywords to 'get_multiple_listings_by_keyword()'
    get_multiple_listings_by_keyword(user_input_search_keywords)
    create_db()

