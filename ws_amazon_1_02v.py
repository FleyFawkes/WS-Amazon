from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# TODO to finish:
# product details:
#     best seller rank
#     manufacturer
#     dimensions
#
# fix else product_stock exception. -
# File "./ws_amazon_1_02v.py", line 95, in main
#     stock_product = 'https://www.amazon.com/'+multi_seller_link['href']
# TypeError: list indices must be integers or slices, not str
#
# fix "synchronous xmlhttprequest on the main thread is deprecated" bug. I'm downloading some
#   script from amazon, somewhere one of the tags has script which starts jquery.
#
# sometimes image_url is : data:image/webp;base64... and go on on on on , its working, but site
# it redirects to is not protected and is not amazon?


def main():
    options = Options()
    options.add_argument('--incognito')
    options.headless = False
    options.page_load_strategy = 'normal'
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    index_2 = f'{index}'
    url = category[f'{category_2[index_2]}']
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')  # multi_valued_attributes=None
    results = soup.find_all('div', {'data-component-type': 's-search-result'})
    master_list = []
    item_url_list = []

    for result in results:
        data_dict = {}
        try:
            data_dict['name'] = result.find('span', {'class': 'a-size-base-plus a-color-base a-text-normal'}).text
        except:
            data_dict['name'] = result.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}).text
        try:
            price = result.find('span', {'class': 'a-offscreen'}).text
            price = price.replace('$', '')
            price = float(price)
            data_dict['price_$'] = price
        except:
            data_dict['price_$'] = float(0)
        try:
            rating = result.find('span', {'class': 'a-icon-alt'}).text
            rating = rating.split()
            rating = float(rating[0])
            data_dict['rating_out_of_5'] = rating
        except:
            data_dict['rating_out_of_5'] = 'None'
        data_dict['item_url'] = 'https://www.amazon.com/'+result.find('a', {'class': 'a-link-normal a-text-normal'})['href']
        item_url_list.append(data_dict['item_url'])
        rews = result.find_all('span', {'class': 'a-size-base'})
        for rew in rews:
            if len(rew['class']) == 1:
                number = rew.text
                number = number.replace(',', '')
                try:
                    number = int(number)
                    if isinstance(number, int):
                        data_dict['reviews'] = number
                except:
                    continue
        master_list.append(data_dict)

    a = 0  # master_list index for dictionaries to iterate through.

    for url in item_url_list:
        driver.get(url)
        soup_product = BeautifulSoup(driver.page_source, 'html.parser')
        for product in soup_product:
            try:
                img_product = product.find('img', {'id': 'landingImage'})['src']
            except:
                img_product = 'None'
            if 'img_url' not in master_list[a]:
                master_list[a].setdefault('img_url', img_product)
            try:
                brand_product = product.find('a', {'id': 'bylineInfo'})['href']
            except:
                brand_product = 'None'
                if 'brand_url' not in master_list[a]:
                    master_list[a].setdefault('brand_url', brand_product)
            if 'brand_url' not in master_list[a]:
                master_list[a].setdefault('brand_url', 'https://www.amazon.com/'+brand_product)
            try:
                stock_product = product.find('span', {'class': 'a-size-medium a-color-success'}).text
            except:
                try:
                    stock_product = product.find('span', {'class': 'a-color-price a-text-bold'}).text
                except AttributeError:
                    stock_product = 'None'
            else:
                try:
                    multi_seller_link = product.find_all('a')
                    for link in multi_seller_link:
                        if link.text == 'these sellers':
                            stock_product = 'https://www.amazon.com/'+link['href']
                except TypeError:
                    stock_product = 'TypeError'
            if 'in_stock' not in master_list[a]:
                stock_product_form_1 = stock_product.replace('\n', '')
                master_list[a].setdefault('in_stock', stock_product_form_1)
            product_details = product.find('div', {'id': 'detailBulletsWrapper_feature_div'})

        # add product detail stuff
        a += 1

    driver.quit()

    amazon_df = pd.DataFrame(master_list)
    amazon_df.to_csv(f'ws_amazon_1_{keyword}.csv', index=False)


if __name__ == '__main__':
    print('type a searching word:')
    keyword = input()
    category = {'All': f'https://www.amazon.com/s?k={keyword}&ref=nb_sb_noss_2',
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
        'Video Games': f'https://www.amazon.com/s?k={keyword}&i=videogames-intl-ship&ref=nb_sb_noss',}
    category_2 = {'0': 'All', '1': 'Arts & Crafts', '2': 'Automotive', '3': 'Baby', '4': 'Beauty & Personal Care',
        '5': 'Books',
        '6': 'Computers', '7': 'Digital Music', '8': 'Electronics',
        '9': 'Kindle Store', '10': 'Prime Video', '11': 'Womens Fashion', '12': 'Mens Fashion', '13': 'Girls Fashion',
        '14': 'Boys Fashion', '15': 'Deals', '16': 'Health & Household',
        '17': 'Home & Kitchen', '18': 'Industrial & Scientific', '19': 'Luggage', '20': 'Movies & TV',
        '21': 'Music, CDs & Vinyl',
        '22': 'Pet Supplies', '23': 'Software', '24': 'Sports & Outdoors',
        '25': 'Tools & Home Improvement', '26': 'Toys & Games', '27': 'Video Games'}
    print('Select the category of the search, by typing the index of the category in number.\n'
          f'{category_2}')
    index = int(input())
    main()
