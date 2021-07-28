
def page_hopping(page_number: int, soup, driver) -> int:
    """page changing mechanism"""
    url_2 = soup.find('ul', {'class': 'a-pagination'})
    url_2_a = url_2.find_all('a')
    if 'page=' not in driver.current_url:
        for link_a in url_2_a:
            if link_a.text == '2':
                url_2_link = 'https://www.amazon.com/' + \
                    link_a['href']
                page_number += 1
                driver.get(url_2_link)
    if f'page={page_number}' in driver.current_url:
        link_page = driver.current_url
        page_number_2 = page_number + 1
        link_page_2 = link_page.replace(
            f'page={page_number}', f'page={page_number_2}')
        link_page_3 = link_page_2.replace(
            f'sr_pg_{page_number}', f'sr_pg_{page_number_2}')
        page_number += 1
        driver.get(link_page_3)
    return page_number


def comprehensive_search(item_url_list: list, master_list: list, a: int, driver, tqdm, BeautifulSoup) -> None:
    """iterating over item urls for more data:
    a: index of master list"""
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
