from utils.amazon_shop import *
from utils.inputs import *
from utils.processing import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
from time import sleep

#TODO: product details + more

def web_scrape(category_1, category_2, keyword, index, quick_search, scrape, datatype):
    options = Options()
    options.add_argument('--incognito')
    options.headless = True
    options.page_load_strategy = 'eager'

    url = category_1[f'{category_2[index]}']

    with WebDriverContext(webdriver.Chrome(ChromeDriverManager().install(), options=options)) as driver:
        for i in range(10):  # amazon bot solution for scraping, open new tab
            driver.get(url)
            captcha_bot = "Sorry, we just need to make sure you're not a robot. For best results, please make sure your browser is accepting cookies."
            check = driver.page_source
            if captcha_bot not in check:
                break
            sleep(2)

        master_list = []  # list of dictionaries for data
        a = 0  # master_list index for dictionaries to iterate through
        item_url_list = []  # list of item urls for data
        # one of number limits used in number of scrapes. Scrape input is second one
        number_on_site = 1
        page_number = 1  # number used for page hopping

        print('initializing, please wait.')
        pbar = tqdm(total=scrape)  # load bar 1

        while number_on_site < scrape:  # scraping amazon products
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            results = soup.find_all(
                'div', {'data-component-type': 's-search-result'})
            for result in results:
                data_dict = {}
                data_dict['keyword'] = keyword
                data_dict['category'] = category_2[index]
                try:
                    data_dict['name'] = result.find(
                        'span', {'class': 'a-size-base-plus a-color-base a-text-normal'}).text
                except:
                    data_dict['name'] = result.find(
                        'span', {'class': 'a-size-medium a-color-base a-text-normal'}).text
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
                                        result.find(
                                            'a', {'class': 'a-link-normal a-text-normal'})['href']
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
                page_number = page_hopping(page_number, soup, driver)
            else:
                break
        pbar.close()

        if quick_search:  # determines quick or comprehensive search, meaning, iterating over item urls for more info
            pass
        else:
            print('collecting entries')
            pbar_2 = tqdm(total=len(item_url_list))  # load bar 2
            for url_3 in item_url_list:
                driver.get(url_3)
                soup_product = BeautifulSoup(driver.page_source, 'html.parser')
                for product in soup_product:
                    try:
                        img_product = product.find(
                            'img', {'id': 'landingImage'})['src']
                    except:
                        img_product = 'None'
                    if 'img_url' not in master_list[a].keys():
                        master_list[a].setdefault('img_url', img_product)
                    try:
                        brand_product = product.find(
                            'a', {'id': 'bylineInfo'})['href']
                    except:
                        brand_product = 'None'
                        if 'brand_url' not in master_list[a].keys():
                            master_list[a].setdefault(
                                'brand_url', brand_product)
                    if 'brand_url' not in master_list[a].keys():
                        master_list[a].setdefault(
                            'brand_url', 'https://www.amazon.com/' + brand_product)
                    try:
                        stock_product = product.find(
                            'span', {'class': 'a-size-medium a-color-success'}).text
                    except:
                        try:
                            stock_product = product.find(
                                'span', {'class': 'a-color-price a-text-bold'}).text
                        except AttributeError:
                            stock_product = 'None'
                    else:
                        try:
                            multi_seller_link = product.find_all('a')
                            for link in multi_seller_link:
                                if link.text == 'these sellers':
                                    stock_product = 'https://www.amazon.com/' + \
                                        link['href']
                        except TypeError:
                            stock_product = 'TypeError'
                    if 'in_stock' not in master_list[a].keys():
                        stock_product_form_1 = stock_product.replace('\n', '')
                        master_list[a].setdefault(
                            'in_stock', stock_product_form_1)
                    product_details = product.find(
                        'div', {'id': 'detailBulletsWrapper_feature_div'})
                a += 1
                pbar_2.update(1)
            pbar_2.close()

    save_data(master_list, keyword, datatype)
    print('Done')


def main():
    category_2 = categories_2()
    keyword, index, quick_search, scrape, datatype = inputs(categories_2())
    category_1 = categories_1(keyword)
    web_scrape(category_1, category_2, keyword,
               index, quick_search, scrape, datatype)


if __name__ == '__main__':
    main()
