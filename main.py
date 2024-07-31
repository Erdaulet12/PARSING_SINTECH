"""PARSING"""

import pandas as pd
from bs4 import BeautifulSoup
import requests

URL = 'https://sintech.kz/'

response = requests.get(URL)
html_content = response.content
soup = BeautifulSoup(html_content, 'html.parser')


def extract_categories(soup):
    """Extracting categories

    Args:
        soup (None): BeautifulSoup

    Returns:
        Categories (String): Categories
    """
    categories = []
    main_categories = soup.find_all('div', class_='revlevel_1')

    for main_category in main_categories:
        main_category_title = main_category.find(
            'div', class_='title').get_text(strip=True)
        subcategories = main_category.find('div', class_='childrenList')

        if subcategories:
            subcategory_list = []
            subcategory_items = subcategories.find_all('li', class_='glavli')

            for subcategory in subcategory_items:
                subcategory_title = subcategory.find('a').get_text(strip=True)
                sub_subcategories = subcategory.find_all('li')

                if sub_subcategories:
                    sub_subcategory_list = []
                    for sub_subcategory in sub_subcategories:
                        sub_subcategory_title = sub_subcategory.find(
                            'a').get_text(strip=True)
                        sub_subcategory_list.append(sub_subcategory_title)
                    subcategory_list.append(
                        {'subcategory': subcategory_title, 'sub_subcategories': sub_subcategory_list})
                else:
                    subcategory_list.append(
                        {'subcategory': subcategory_title, 'sub_subcategories': []})
            categories.append(
                {'main_category': main_category_title, 'subcategories': subcategory_list})
        else:
            categories.append(
                {'main_category': main_category_title, 'subcategories': []})

    return categories


if __name__ == "__main__":

    data = []

    categories = extract_categories(soup)

    for category in categories:
        main_category = category['main_category']
        for subcategory in category['subcategories']:
            subcategory_name = subcategory['subcategory']
            if subcategory['sub_subcategories']:
                for sub_subcategory in subcategory['sub_subcategories']:
                    data.append(
                        [main_category, subcategory_name, sub_subcategory])
            else:
                data.append([main_category, subcategory_name, ""])

    df = pd.DataFrame(
        data, columns=["Главная категория", "Подкатегория", "Под-подкатегория"])

    df.to_excel('categories.xlsx', index=False)

    print("Операция завершена. Данные успешно записаны в categories.xlsx")
