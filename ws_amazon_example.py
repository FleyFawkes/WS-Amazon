from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def main():
    options = Options()
    options.add_argument('--incognito')
    options.headless = True
    options.page_load_strategy = 'normal'
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    url = f'https://www.amazon.com/s?k={keyword}&ref=nb_sb_noss'
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all('div', {'data-component-type': 's-search-result'})
    master_list = []

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
        master_list.append(data_dict)

    driver.quit()
    amazon_df = pd.DataFrame(master_list)
    amazon_df.to_csv(f'ws_amazon_example_{keyword}.csv', index=False)


if __name__ == '__main__':
    print('write search keyword')
    keyword = input()
    main()
