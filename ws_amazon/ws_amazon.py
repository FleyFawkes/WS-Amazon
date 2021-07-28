from utils.amazon_shop import WebDriverContext
from utils.inputs import inputs, save_data, categories_1, categories_2
from utils.processing import page_hopping, comprehensive_search
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
from time import sleep
from datetime import datetime

# TODO: product details + more


def web_scrape(category_1, category_2, keyword, index, quick_search, scrape):
    options = Options()
    options.add_argument('--incognito')
    options.headless = True
    options.page_load_strategy = 'eager'

    master_list = []  # list of dictionaries for data
    item_url_list = []  # list of item urls for data
    # one of number limits used in number of scrapes. Scrape input is second one
    number_on_site = 1
    page_number = 1  # number used for page hopping
    time = datetime.now().strftime("%H_%M_%S")

    url = category_1[f'{category_2[index]}']

    with WebDriverContext(webdriver.Chrome(ChromeDriverManager().install(), options=options)) as driver:
        for i in range(10):  # amazon bot solution for scraping, open new tab
            driver.get(url)
            captcha_bot = "Sorry, we just need to make sure you're not a robot. For best results, please make sure your browser is accepting cookies."
            check = driver.page_source
            if captcha_bot not in check:
                break
            sleep(2)

        print('initializing, please wait.')
        pbar = tqdm(total=scrape)  # load bar 1

        while number_on_site < scrape:  # quick scraping amazon products
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            results = soup.find_all(
                'div', {'data-component-type': 's-search-result'})
            for result in results:
                data_dict = {}
                data_dict['keyword'] = keyword
                data_dict['category'] = category_2[index]
                data_dict['timestamp'] = time
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

        if not quick_search:  # determines quick or comprehensive search
            comprehensive_search(item_url_list, master_list,
                                 0, driver, tqdm, BeautifulSoup)

    return master_list


def main():
    category_2 = categories_2()
    keyword, index, quick_search, scrape, datatype = inputs(categories_2())
    category_1 = categories_1(keyword)
    master_list = web_scrape(category_1, category_2, keyword,
                             index, quick_search, scrape)
    save_data(master_list, keyword, datatype)
    print('Done')


if __name__ == '__main__':
    main()
