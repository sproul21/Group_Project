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
        category = "Over Ear Headphones"
        return category
    elif choice == "2":
        category = "USB Microphones"
        return category
    elif choice == "3":
        category = "1080p Webcams"
        return category
    elif choice == "4":
        category = "Capture Cards"
        return category
    elif choice == "5":
        category = "8-channel Audio Mixers"
        return category
    elif choice == "6":
        category = "Gaming Laptops"
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
