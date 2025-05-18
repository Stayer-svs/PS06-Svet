
import requests
from bs4 import BeautifulSoup
import csv

# Ссылки на категории
categories = [
    "https://www.divan.ru/category/potolocnye-svetilniki",
    "https://www.divan.ru/category/ulichnye-svetilniki",
    "https://www.divan.ru/category/podvesnye-svetilniki",
    "https://www.divan.ru/category/podvesnye-svetilniki/page-2",
    "https://www.divan.ru/category/podvesnye-svetilniki/page-3",
    "https://www.divan.ru/category/lyustry",
    "https://www.divan.ru/category/torshery",
    "https://www.divan.ru/category/nastolnye-lampy",
    "https://www.divan.ru/category/nastolnye-lampy/page-2",
    "https://www.divan.ru/category/bra"
]

# Функция для парсинга одной категории
def parse_category(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Ошибка при запросе {url}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    products = []

    # Находим все товары на странице
    for item in soup.find_all("div", class_="lsooF"):
        name_tag = item.find("span", itemprop="name")
        price_tag = item.find("meta", itemprop="price")
        link_tag = item.find("link", itemprop="url")

        if name_tag and price_tag and link_tag:
            name = name_tag.text.strip()
            price = price_tag["content"]
            link = link_tag["href"]
            products.append([name, price, link])

    return products

# Запись данных в CSV
with open("lightings.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Название", "Цена", "Ссылка"])

    for category in categories:
        print(f"Парсим категорию: {category}")
        products = parse_category(category)
        writer.writerows(products)

print("Парсинг завершен, данные сохранены в 'lightings.csv'")
