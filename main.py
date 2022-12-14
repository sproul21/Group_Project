import requests
from bs4 import BeautifulSoup
import sqlite3


def main():
    HEADERS_FOR_GET_REQ = (
        {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/101.0.4951.54 Safari/537.36 ', 'Accept-Language': 'en-US, en;q=0.5'}
    )

    conn = sqlite3.connect('headphones.db')
    cursor = conn.cursor()
    conn.execute('''CREATE TABLE IF NOT EXISTS headphones (
                                             product_name TEXT,
                                             rating REAL,
                                             num_ratings INTEGER,
                                             price REAL,
                                             product_url TEXT
                                         ); ''')
    # Set the URL we want to scrape
    url = "https://www.amazon.com/s?k=over+ear+headphones"

    # Make a request to the URL
    response = requests.get(url, headers=HEADERS_FOR_GET_REQ)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract the product details we are interested in
    products = soup.find_all('div', {'class': 's-result-item', 'data-component-type': 's-search-result'})

    # Loop through the products and extract the details we want
    for product in products:
        product_name = product.find("span", {"class": "a-size-medium a-color-base a-text-normal"}).text
        rating = product.find('i', {'class': 'a-icon'}).text
        num_ratings = product.find('span', {'class': 'a-size-base s-underline-text'}).text
        price_integer = product.find('span', {'class': 'a-price-whole'}).text
        price_decimal = product.find('span', {'class': 'a-price-fraction'}).text
        price = price_integer + price_decimal
        product_url_segment = product.h2.a['href']
        product_url = 'https://amazon.com' + product_url_segment

        cursor.execute("""INSERT INTO headphones (product_name, rating, num_ratings, price, product_url) VALUES (?, 
        ?, ?, ?, ?)""", (product_name, rating, num_ratings, price, product_url))

        conn.commit()

        # conn.close()
        # Print the details we extracted
        # print(product_name)
        # print(rating)
        # print(num_ratings)
        # print(price)
        # print(product_url)


if __name__ == '__main__':
    main()
