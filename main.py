from bs4 import BeautifulSoup
import requests
import csv

URL = 'https://auto.ria.com/uk/newauto/category-legkovie/marka-volkswagen/'
HEADERS = {
    "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0"}
HOST = 'https://auto.ria.com'


def get_html(url, params=None):
    return requests.get(url, headers=HEADERS, params=params)


def get_cars(content):
    soup = BeautifulSoup(content, 'html.parser')
    items = soup.find_all("section", class_="proposition")
    cars = []
    for item in items:
        usd_price, uah_price = item.find("div", "proposition_price").get_text(strip=True).split("•")
        car = {"title": item.find("h3", "proposition_name").get_text(strip=True),
               "city": item.find("span", "item region").get_text(strip=True),
               "link": HOST + item.find("a", "proposition_link").get("href"),
               "usd_price": usd_price,
               "uah_price": uah_price,
               }
        cars.append(car)
    return cars


def save_to_file(cars):
    with open("cars.csv", "w", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["Title",
                         "City",
                         "USD price",
                         "UAH price",
                         "Link",
                         ])
        for car in cars:
            writer.writerow([car.get("title"),
                             car.get("city"),
                             car.get("usd_price"),
                             car.get("uah_price"),
                             car.get("link"),
                             ])


def main():
    html = get_html(URL)
    get_cars(html.text)

    save_to_file(get_cars(html.text))
    print(html)


if __name__ == "__main__":
    main()
