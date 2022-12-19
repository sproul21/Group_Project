import random
import sqlite3


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def find_category():
    print("choose a product category:")
    print("     1. Over Ear Headphones")
    print("     2. USB Microphones")
    print("     3. 1080p Webcams")
    print("     4. Capture Cards")
    print("     5. 8-channel Audio Mixers")
    print("     6. Gaming Laptops")
    choice = input("Input a number")
    choice = choice.strip()
    if choice == "1":
        category = "overearheadphones"
        return category
    elif choice == "2":
        category = "USBmicrophones"
        return category
    elif choice == "3":
        category = "Webcams1080p"
        return category
    elif choice == "4":
        category = "CaptureCards"
        return category
    elif choice == "5":
        category = "EightChannelAudioMixers"
        return category
    elif choice == "6":
        category = "GamingLaptops"
        return category
    else:
        print("Not a valid input")
        find_category()


def find_review():
    choice = input("Enter a target star review (ex. '4.5'):")
    if isfloat(choice) and 0.0 <= float(choice) <= 5.0:
        return choice
    else:
        print("Enter a valid float between 0.0 and 5.0")
        find_review()


def find_equality_operator():
    choice = input("Choose an equality operator (>, <, >=, <=, =):")
    return choice


def find_num_reviews():
    choice = input("Enter a target number of reviews (ex. '1000'):")
    return choice


def find_price():
    choice = input("Enter a target price (ex. '59.99'):")
    return choice


def search_params():
    user_search = []

    category = find_category()
    user_search.append(category)

    review = find_review()
    if review is not None:
        user_search.append(review)

    equality_op = find_equality_operator()
    user_search.append(equality_op)

    num_reviews = find_num_reviews()
    user_search.append(num_reviews)

    equality_op = find_equality_operator()
    user_search.append(equality_op)

    price = find_price()
    user_search.append(price)

    equality_op = find_equality_operator()
    user_search.append(equality_op)

    return user_search
    # print(user_search)


def print_params(user_search):
    print(f'SELECT * FROM {user_search[0]} WHERE rating {user_search[2]} {user_search[1]} AND num_ratings {user_search[4]} {user_search[3]} AND price {user_search[6]} {user_search[5]}')
    parse_string = f'SELECT * FROM {user_search[0]} WHERE rating {user_search[2]} {user_search[1]} AND num_ratings {user_search[4]} {user_search[3]} AND price {user_search[6]} {user_search[5]}'
    return parse_string
def parse(parse_string):
    conn = sqlite3.connect('product_data.db')
    cursor = conn.cursor()

    cursor.execute(f'''{parse_string}''')

    q1_result = cursor.fetchall()
    print_parse(q1_result, parse_string)


def print_parse(result, parse_string):
    random_num = random.randint(1,25)
    with open(f'output_{random_num}.txt', 'w') as f:
        f.write(str(parse_string))
        print("\n")
        for item in result:
            f.write(str(item))
            f.write('\n')

    for item in result:
        print(item)
        print("\n")

def loop():


    while True:
        user_search = search_params()
        parse_string = print_params(user_search)
        parse(parse_string)

        choice = input("Would you like to execute another query (yes/no):")
        if choice == "yes":
            continue
        elif choice == "no":
            print("Exiting program...")
            break
        else:
            print("Please enter a valid response (yes/no)")

    return False