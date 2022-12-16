def extract_product_name(product_html_block):
    product_name = None
    try:
        product_name = product_html_block.h2.text
    except AttributeError:
        print('no product name')
    finally:
        return product_name


def extract_product_ratings(product_html_block):
    product_ratings = None
    try:
        #product_ratings = product_html_block.find('i', {'class': 'a-icon'}).text
        product_ratings = product_html_block.find('span', {'aria-label': True}).text
    except AttributeError:
        print('no rating')
    finally:
        return product_ratings


def extract_product_num_ratings(product_html_block):
    product_num_ratings = None
    try:
        product_num_ratings = product_html_block.find('span', {'class': 'a-size-base s-underline-text'}).text
    except AttributeError:
        print('no num ratings')
    finally:
        return product_num_ratings


def extract_product_price(product_html_block):
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
    product_url = None
    try:
        product_url_segment = product_html_block.h2.a['href']
        product_url = 'https://amazon.com' + product_url_segment
    except AttributeError:
        print('no url')
    finally:
        return product_url

