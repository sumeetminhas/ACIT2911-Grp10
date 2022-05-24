import csv
import json
import os
from werkzeug.utils import secure_filename

products_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'admin-only')
login_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'admin-only', 'creds.json')
transactions_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'admin-only', 'transactions.json')

def read_products():
    with open(os.path.join(products_file_path, 'products.csv'), 'r') as file:
            product_list = list(csv.reader(file))
            images = os.listdir('static/product_image')

            return product_list, images

def read_json():
    with open(transactions_file_path, 'r') as history:
        return json.load(history)

def update_history(list):
    all_history = read_json()
    return none
