from pandas import DataFrame


def save_data(data: list, keyword: any, datatype: str):
    if datatype == "csv":
        amazon_df = DataFrame(data)
        amazon_df.to_csv(f'ws_amazon_{keyword}.csv', index=False)
    elif datatype == "txt":
        pass
    elif datatype == "db":
        pass


def get_data() -> str:
    while True:
        try:
            datatype = {"t": "txt", "c": "csv", "d": "db"}[input().lower()]
            return datatype
        except KeyError:
            print("Invalid input, please enter (t) , (c) or (d)!")


def get_index() -> str:
    while True:
        try:
            index = int(input())
            if index < 0:
                raise ValueError('That\'s not a positive integer!')
            return str(index)
        except ValueError:
            print('That\'s not a positive integer!')


def get_scrape() -> int:
    while True:
        try:
            scrape = int(input())
            if scrape < 1:
                raise ValueError('That\'s not a positive integer!')
            return scrape
        except ValueError:
            print('That\'s not a positive integer!')


def get_quick_search() -> bool:
    while True:
        try:
            quick_search = {"q": True, "c": False}[input().lower()]
            return quick_search
        except KeyError:
            print("Invalid input, please enter (q) or (c)!")


def inputs(category: dict) -> tuple:
    """inputs for scraping:
    keyword, index of category, quick or comprehesive search, no. of entries, how to save the data"""
    print('Type a keyword to search for:')
    keyword = str(input())
    print('Select the category of the search, by typing the index of the category in number:\n'
          f'{category}')
    index = get_index()
    print(
        'Would you like a (q)uick[~50 in 4sec] or (c)omprehensive[~50 in 4mins] search?:')
    quick_search = get_quick_search()
    print('How many entries would you like to get? type in number:')
    scrape = get_scrape()
    print('How should the data be saved? (t)xt, (c)sv or in (d)b?')
    datatype = get_data()
    return keyword, index, quick_search, scrape, datatype


def categories_2() -> dict:
    """categories of amazon products"""
    category_2 = {'0': 'All-only 7 pages of search', '1': 'Arts & Crafts', '2': 'Automotive', '3': 'Baby',
                  '4': 'Beauty & Personal Care', '5': 'Books',
                  '6': 'Computers', '7': 'Digital Music', '8': 'Electronics',
                  '9': 'Kindle Store', '10': 'Prime Video', '11': 'Womens Fashion', '12': 'Mens Fashion',
                  '13': 'Girls Fashion',
                  '14': 'Boys Fashion', '15': 'Deals', '16': 'Health & Household',
                  '17': 'Home & Kitchen', '18': 'Industrial & Scientific', '19': 'Luggage', '20': 'Movies & TV',
                  '21': 'Music, CDs & Vinyl',
                  '22': 'Pet Supplies', '23': 'Software', '24': 'Sports & Outdoors',
                  '25': 'Tools & Home Improvement', '26': 'Toys & Games', '27': 'Video Games'}
    return category_2


def categories_1(keyword: str) -> dict:
    """urls of amazon categories"""
    category_1 = {'All-only 7 pages of search': f'https://www.amazon.com/s?k={keyword}&ref=nb_sb_noss_2',
                  'Arts & Crafts': f'https://www.amazon.com/s?k={keyword}&i=arts-crafts-intlship&ref=nb_sb_noss',
                  'Automotive': f'https://www.amazon.com/s?k={keyword}&i=automotive-intl-ship&ref=nb_sb_noss',
                  'Baby': f'https://www.amazon.com/s?k={keyword}&i=baby-products-intl-ship&ref=nb_sb_noss',
                  'Beauty & Personal Care': f'https://www.amazon.com/s?k={keyword}&i=beauty-intl-ship&ref=nb_sb_noss',
                  'Books': f'https://www.amazon.com/s?k={keyword}&i=stripbooks-intl-ship&ref=nb_sb_noss',
                  'Computers': f'https://www.amazon.com/s?k={keyword}&i=computers-intl-ship&ref=nb_sb_noss',
                  'Digital Music': f'https://www.amazon.com/s?k={keyword}&i=digital-music&ref=nb_sb_noss',
                  'Electronics': f'https://www.amazon.com/s?k={keyword}&i=electronics-intl-ship&ref=nb_sb_noss',
                  'Kindle Store': f'https://www.amazon.com/s?k={keyword}&i=digital-text&ref=nb_sb_noss',
                  'Prime Video': f'https://www.amazon.com/s?k={keyword}&i=instant-video&ref=nb_sb_noss',
                  'Womens Fashion': f'https://www.amazon.com/s?k={keyword}&i=fashion-womens-intl-ship&ref=nb_sb_noss',
                  'Mens Fashion': f'https://www.amazon.com/s?k={keyword}&i=fashion-mens-intl-ship&ref=nb_sb_noss',
                  'Girls Fashion': f'https://www.amazon.com/s?k={keyword}&i=fashion-girls-intl-ship&ref=nb_sb_noss',
                  'Boys Fashion': f'https://www.amazon.com/s?k={keyword}&i=fashion-boys-intl-ship&ref=nb_sb_noss',
                  'Deals': f'https://www.amazon.com/s?k={keyword}&i=deals-intl-ship&ref=nb_sb_noss',
                  'Health & Household': f'https://www.amazon.com/s?k={keyword}&i=hpc-intl-ship&ref=nb_sb_noss',
                  'Home & Kitchen': f'https://www.amazon.com/s?k={keyword}&i=kitchen-intl-ship&ref=nb_sb_noss',
                  'Industrial & Scientific': f'https://www.amazon.com/s?k={keyword}&i=industrial-intl-ship&ref=nb_sb_noss',
                  'Luggage': f'https://www.amazon.com/s?k={keyword}&i=luggage-intl-ship&ref=nb_sb_noss',
                  'Movies & TV': f'https://www.amazon.com/s?k={keyword}&i=movies-tv-intl-ship&ref=nb_sb_noss',
                  'Music, CDs & Vinyl': f'https://www.amazon.com/s?k={keyword}&i=music-intl-ship&ref=nb_sb_noss',
                  'Pet Supplies': f'https://www.amazon.com/s?k={keyword}&i=pets-intl-ship&ref=nb_sb_noss',
                  'Software': f'https://www.amazon.com/s?k={keyword}&i=software-intl-ship&ref=nb_sb_noss',
                  'Sports & Outdoors': f'https://www.amazon.com/s?k={keyword}&i=sporting-intl-ship&ref=nb_sb_noss',
                  'Tools & Home Improvement': f'https://www.amazon.com/s?k={keyword}&i=tools-intl-ship&ref=nb_sb_noss',
                  'Toys & Games': f'https://www.amazon.com/s?k={keyword}&i=toys-and-games-intl-ship&ref=nb_sb_noss',
                  'Video Games': f'https://www.amazon.com/s?k={keyword}&i=videogames-intl-ship&ref=nb_sb_noss', }
    return category_1
