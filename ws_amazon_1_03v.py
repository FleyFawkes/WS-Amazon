from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm

# TODO to finish:
"""
product details:
    best seller rank
    manufacturer
    dimensions

fix "synchronous xmlhttprequest on the main thread is deprecated" bug. I'm downloading some
  script from amazon, somewhere one of the tags has script which starts jquery.
"""


def web_scrape(category, category_2):
    options = Options()
    options.add_argument('--incognito')
    options.headless = True
    options.page_load_strategy = 'eager'
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    master_list = []  # list of dictionaries for data
    item_url_list = []  # list of item urls for data
    number_on_site = 1  # one of number limit used in number of scrapes. Scrape input is second one
    page_number = 1  # number used for page hopping
    a = 0  # master_list index for dictionaries to iterate through

    index_2 = f'{index}'
    url = category[f'{category_2[index_2]}']
    driver.get(url)

    print('initializing, please wait.')
    pbar = tqdm(total=scrape)  # load bar 1

    while number_on_site < scrape:  # user input entries mechanism
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')  # multi_valued_attributes=None
        results = soup.find_all('div', {'data-component-type': 's-search-result'})
        for result in results:
            data_dict = {}
            data_dict['keyword'] = keyword
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
            data_dict['item_url'] = 'https://www.amazon.com/' + \
                                    result.find('a', {'class': 'a-link-normal a-text-normal'})['href']
            item_url_list.append(data_dict['item_url'])
            if data_dict['rating_out_of_5'] == 'None':
                data_dict['reviews'] = 0
            else:
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
            number_on_site += 1
            pbar.update(1)
            if number_on_site > scrape:
                break
        if number_on_site < scrape:  # page hopping mechanism
            url_2 = soup.find('ul', {'class': 'a-pagination'})
            url_2_a = url_2.find_all('a')
            if 'page=' not in driver.current_url:
                for link_a in url_2_a:
                    if link_a.text == '2':
                        url_2_link = 'https://www.amazon.com/' + link_a['href']
                        page_number += 1
                        driver.get(url_2_link)
            if f'page={page_number}' in driver.current_url:
                link_page = driver.current_url
                page_number_2 = page_number + 1
                link_page_2 = link_page.replace(f'page={page_number}', f'page={page_number_2}')
                link_page_3 = link_page_2.replace(f'sr_pg_{page_number}', f'sr_pg_{page_number_2}')
                page_number += 1
                driver.get(link_page_3)
        else:
            break

    pbar.close()

    if quick_search:  # determines quick or comprehensive search.
        pass
    else:
        print('collecting entries')
        pbar_2 = tqdm(total=len(item_url_list))  # load bar 2
        for url_3 in item_url_list:
            driver.get(url_3)
            soup_product = BeautifulSoup(driver.page_source, 'html.parser')
            for product in soup_product:
                try:
                    img_product = product.find('img', {'id': 'landingImage'})['src']
                except:
                    img_product = 'None'
                if 'img_url' not in master_list[a].keys():
                    master_list[a].setdefault('img_url', img_product)
                try:
                    brand_product = product.find('a', {'id': 'bylineInfo'})['href']
                except:
                    brand_product = 'None'
                    if 'brand_url' not in master_list[a].keys():
                        master_list[a].setdefault('brand_url', brand_product)
                if 'brand_url' not in master_list[a].keys():
                    master_list[a].setdefault('brand_url', 'https://www.amazon.com/' + brand_product)
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
                                stock_product = 'https://www.amazon.com/' + link['href']
                    except TypeError:
                        stock_product = 'TypeError'
                if 'in_stock' not in master_list[a].keys():
                    stock_product_form_1 = stock_product.replace('\n', '')
                    master_list[a].setdefault('in_stock', stock_product_form_1)
                product_details = product.find('div', {'id': 'detailBulletsWrapper_feature_div'})
            a += 1
            pbar_2.update(1)
        pbar_2.close()

    driver.quit()
    get_data(master_list)
    print('Done')


def get_data(data):
    amazon_df = pd.DataFrame(data)
    amazon_df.to_csv(f'ws_amazon_1_{keyword}.csv', index=False)


def get_index():
    global index
    while True:
        try:
            index = int(input())
            return index
        except ValueError:
            print('That\'s not an integer!')


def get_scrape():
    global scrape
    while True:
        try:
            scrape = int(input())
            return scrape
        except ValueError:
            print('That\'s not an integer!')


def get_quick_search():
    global quick_search
    while True:
        try:
            quick_search = {"q": True, "c": False}[input().lower()]
            return quick_search
        except KeyError:
            print("Invalid input please enter (q) or (c)!")


def inputs(category_2):
    global keyword
    print('Type a keyword to search:')
    keyword = str(input())
    print('Select the category of the search, by typing the index of the category in number:\n'
          f'{category_2}')
    get_index()
    print('Would you like a (q)uick[~50 in 4sec] or (c)omprehensive[~50 in 4mins] search?:')
    get_quick_search()
    print('How many entries would you like to get? type in number:')
    get_scrape()


def main():
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
    inputs(category_2)
    category = {'All-only 7 pages of search': f'https://www.amazon.com/s?k={keyword}&ref=nb_sb_noss_2',
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
    web_scrape(category, category_2)


if __name__ == '__main__':
    main()
