import csv
import json


def convert_brand_data_from_json(json_file_path: str):
    csv_file = open(json_file_path.replace('.json', '.csv'), 'w', encoding='utf-8')
    writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    writer.writerow(['Brand', 'Products', 'Categories'])

    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)

        for brand in json_data['Brands']:
            data = json_data['Brands'][brand]
            products = "|".join(data['Products'])
            categories = '|'.join(data['Product Categories'])
            writer.writerow([brand, products, categories])

    csv_file.close()


def convert_categories_data_from_json(json_categories_path: str):
    csv_file = open(json_categories_path.replace('.json', '.csv'), 'w', encoding='utf-8')
    writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    writer.writerow(['Category', 'Image URL'])

    with open(json_categories_path, 'r') as json_file:
        json_data = json.load(json_file)
        for category in json_data.keys():
            writer.writerow([category, json_data[category]])

    csv_file.close()

if __name__ == '__main__':
    #convert_brand_data_from_json('brands.json')
    convert_categories_data_from_json('categories.json')