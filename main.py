import parse_functions
import scrape_functions


def main():
    scrape_functions.fill_database()

    while True:
        result = parse_functions.loop()
        if result is False:
            break

if __name__ == '__main__':
    main()

