import csv
from encodings import utf_8
import json
import os
from cart import Cart
from werkzeug.utils import secure_filename

products_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'admin-only')
login_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'admin-only', 'creds.json')
transactions_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'admin-only', 'transactions.json')

def read_products():
    with open(os.path.join(products_file_path, 'products.csv'), 'r') as file:
            print(file)
            print(type(file))
            product_list = list(csv.reader(file))
            images = os.listdir('static/product_image')
            image_list = []
            for image in images:
                image_list.append(image[:-4])

            return product_list, image_list

def read_json():
    with open(transactions_file_path, 'r') as history:
        return json.load(history)

def add_to_history(transaction, history):
    history.append(transaction)
    with open(transactions_file_path, 'w') as file:
        json.dump(history, file)

def class_to_dict(instance):
    if isinstance(instance, Cart):
        list_html = "<ul class='final-order'>"
        for item in instance.list:
            li_item = f'<div>{item[1]}: {item[2]}</div>'
            list_html += li_item
        list_html += "</ul>"

        return list_html, instance.total

def update_products(products):
    with open(os.path.join(products_file_path, 'products2.csv'), 'w', encoding="UTF8", newline='') as file:
        writer = csv.writer(file)
        for product in products:
            writer.writerow(product)
