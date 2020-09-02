import datetime
import json
import urllib.request
from typing import Generator
from bs4 import BeautifulSoup

brand_home_url = 'https://www.manualslib.com/brand/'
base_url = 'https://www.manualslib.com'
b_url = 'https://www.manualslib.com/brand/acer/'


def make_soup(input_url):
    html_headers = {'User-Agent': 'Mozilla/5.0'
                                  'KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                    'Accept-Encoding': 'none',
                    'Accept-Language': 'en-US,en;q=0.8',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Connection': 'keep-alive'}
    req = urllib.request.Request(input_url, headers=html_headers)
    return BeautifulSoup(urllib.request.urlopen(req).read(), "lxml")


def get_category_links_from_brand_page(soup) -> {}:
    return {d.text.strip(): "".join([base_url, d.find('a')['href']]) for d in soup.findAll('div', class_='cathead')}


def get_brand_alpha_urls() -> {}:
    return ["".join([base_url, link['href']]) for link in make_soup(brand_home_url).find('div', class_='bmap').findAll('a')]


def get_brands() -> Generator[tuple, None, None]:
    for brand_alpha_url in get_brand_alpha_urls():
        for row in make_soup(brand_alpha_url).find('table',  class_='table table-striped table-hover table-condensedd').findAll('tr'):
            brand_link = row.find('td').find('a')  # Brand Name, Brand Link
            yield brand_link.text.strip(), "".join([base_url, brand_link['href']])


def run():
    start_time = datetime.datetime.now()

    brand_map = {}
    category_image_map = {}

    brand_count = 1
    for brand_name, brand_link in get_brands():
        print("Parsing Brand: " + brand_name + f" ({brand_count})")
        brand_soup = make_soup(brand_link)
        carousel = brand_soup.find('div', id='carousel')

        if carousel:
            for image in carousel.findAll('a'):
                if image.text.strip() not in category_image_map:
                    category_name = image.text.strip()
                    category_image_url = "".join([base_url, image.find('img')['src']])
                    category_image_map[category_name] = category_image_url
                    print(f"Added category: {category_name} URL: {category_image_url}")

        brand_products = [b.text.strip() for b in brand_soup.findAll('td', class_='product-col')[:5]]
        brand_categories = list(get_category_links_from_brand_page(brand_soup).keys())
        brand_map[brand_name] = {'Products': brand_products, 'Product Categories': brand_categories}
        brand_count += 1

    with open('brands.json', 'w') as fp:
        json.dump({'Brands': brand_map}, fp)

    with open('categories.json', 'w') as f:
        json.dump(category_image_map, f)

    print("Execution time: " + str(datetime.datetime.now() - start_time))


if __name__ == '__main__':
    run()



