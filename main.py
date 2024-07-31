"""
PARSING SINTECH
main.py
"""

from bs4 import BeautifulSoup
import pandas as pd
import requests

URL = 'https://sintech.kz/'

response = requests.get(URL)
html_content = response.content
soup = BeautifulSoup(html_content, 'html.parser')


def extract_categories(soup):
    """Extracting categories

    Args:
        soup (None): Beautiful soup

    Returns:
        Categories(String): Categories
    """
    
    categories = []
    main_categories = soup.find_all('div', class_='revlevel_1')

    for main_category in main_categories:
        main_category_title = main_category.find(
            'div', class_='title').get_text(strip=True)
        main_category_link = main_category.find('a')['href']
        subcategories = main_category.find('div', class_='childrenList')

        if subcategories:
            subcategory_list = []
            subcategory_items = subcategories.find_all('li', class_='glavli')

            for subcategory in subcategory_items:
                subcategory_title = subcategory.find('a').get_text(strip=True)
                subcategory_link = subcategory.find('a')['href']
                sub_subcategories = subcategory.find_all('li')

                if sub_subcategories:
                    sub_subcategory_list = []
                    for sub_subcategory in sub_subcategories:
                        sub_subcategory_title = sub_subcategory.find(
                            'a').get_text(strip=True)
                        sub_subcategory_link = sub_subcategory.find('a')[
                            'href']
                        products = extract_products(sub_subcategory_link)
                        sub_subcategory_list.append(
                            {'sub_subcategory': sub_subcategory_title, 'link': sub_subcategory_link, 'products': products})
                    subcategory_list.append(
                        {'subcategory': subcategory_title, 'link': subcategory_link, 'sub_subcategories': sub_subcategory_list})
                else:
                    products = extract_products(subcategory_link)
                    subcategory_list.append(
                        {'subcategory': subcategory_title, 'link': subcategory_link, 'sub_subcategories': [], 'products': products})
            categories.append({'main_category': main_category_title,
                              'link': main_category_link, 'subcategories': subcategory_list})
        else:
            categories.append({'main_category': main_category_title,
                              'link': main_category_link, 'subcategories': []})

    return categories



def extract_products(url):
    """None"""
    return []

if __name__=="__main__":
    categories = extract_categories(soup)

    data = []

    for category in categories:
        main_category = category['main_category']
        main_category_link = category['link']
        for subcategory in category['subcategories']:
            subcategory_name = subcategory['subcategory']
            subcategory_link = subcategory['link']
            if subcategory['sub_subcategories']:
                for sub_subcategory in subcategory['sub_subcategories']:
                    sub_subcategory_name = sub_subcategory['sub_subcategory']
                    sub_subcategory_link = sub_subcategory['link']
                    products = sub_subcategory['products']
                    if products:
                        for product in products:
                            data.append([main_category, main_category_link, subcategory_name,
                                        subcategory_link, sub_subcategory_name, sub_subcategory_link, product])
                    else:
                        data.append([main_category, main_category_link, subcategory_name,
                                    subcategory_link, sub_subcategory_name, sub_subcategory_link, ""])
            else:
                products = subcategory['products']
                if products:
                    for product in products:
                        data.append([main_category, main_category_link,
                                    subcategory_name, subcategory_link, "", "", product])
                else:
                    data.append([main_category, main_category_link,
                                subcategory_name, subcategory_link, "", "", ""])

    df = pd.DataFrame(data, columns=["Главная категория", "Ссылка глав.категории", "Подкатегория",
                    "Ссылка подкатегории", "Под-подкатегория", "Ссылка под-подкатегории", "Товар"])

    df.to_excel('categories.xlsx', index=False)

    print("Данные успешно записаны в categories.xlsx")
