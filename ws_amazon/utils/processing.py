
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
