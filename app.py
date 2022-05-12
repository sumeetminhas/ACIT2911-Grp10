from ssl import HAS_TLSv1_1
from flask import Flask, render_template, request, redirect, url_for, flash, session
from cart import Cart
import os
import json
import csv

app = Flask(__name__)
app.secret_key = "super-secret-key"

LIVE_SESSIONS = []
active_cart = []

products_file_path = os.path.join('admin-only', 'products.csv')
login_file_path = os.path.join('admin-only', 'creds.json')


@app.route('/')
def homepage():
    if len(LIVE_SESSIONS) == 0:
        LIVE_SESSIONS.append(Cart(request.remote_addr))
    for user in LIVE_SESSIONS:
        if user.owner == request.remote_addr:
            break
        else: LIVE_SESSIONS.append(Cart(request.remote_addr))
    
    print(LIVE_SESSIONS)
    return render_template('/home.html', users=LIVE_SESSIONS)


@app.route('/products')
def products():
    if os.path.exists(products_file_path):
        with open(products_file_path, 'r') as file:
            product_list = list(csv.reader(file))
            images = os.listdir('static/product_image')

        return render_template('/products.html', products=product_list, image_list=images, users=LIVE_SESSIONS)
    else:
        return "<h1>No Products to display</h1><h2>Please visit us at a later time.</h2>"



@app.route('/admin')
def admin():
    if os.path.exists(login_file_path):
        with open(login_file_path, 'r') as creds:
                admin_list = json.loads(creds.read())
                for admin in admin_list:
                    if admin['email'] in session.values():
                        return render_template('admin_dashboard.html', user=admin['name'])
                return render_template('admin-login.html')
    else:
        return '<h1>Admin Portal not set up. Please use static features. '


@app.route('/about')
def about():
    for user in LIVE_SESSIONS:
        if user.owner == request.remote_addr:
            for item in user.list:
                print(item)
    return render_template('about.html', users=LIVE_SESSIONS)


@app.route('/admin/dashboard', methods=['POST'])
def dashboard():
    if request.method == 'POST':
        with open('creds.json', 'r') as creds:
            admin_list = json.loads(creds.read())
            email, password = request.form['email'], request.form['password']
            for admin in admin_list:
                if admin['email'] in session.values(): 
                    return render_template('admin_dashboard.html', user=admin['name'])
                elif email == admin['email'] and password == admin['password']:
                    session["email"] = email
                    for item in session.values(): print(item)
                    return render_template('admin_dashboard.html', user=admin['name'])
            
            flash("Incorrect email or password. Try Again..")
            return redirect('/admin')

@app.route("/add-to-cart", methods = ['GET', 'POST'])
def add_to_cart():
    if request.method == 'POST':
        p_id = request.form['p-id']
        p_name = request.form['p-name']
        p_cost = request.form['p-cost']
        p_desc = request.form['p-desc']
        p_cat = request.form['p-cat']
        product = [p_id, p_name, p_cost, p_desc, p_cat]

        for user in LIVE_SESSIONS:
            if user.owner == request.remote_addr:
                user.list.append(product)
    
    return redirect(request.referrer)


@app.route("/del-cart-item", methods = ["GET", "POST"])
def del_cart_item():
    if request.method == 'POST':
        p_id = request.form['p-id']
        p_name = request.form['p-name']
        p_cost = request.form['p-cost']
        p_desc = request.form['p-desc']
        p_cat = request.form['p-cat']
        product = [p_id, p_name, p_cost, p_desc, p_cat]

        for user in LIVE_SESSIONS:
            if user.owner == request.remote_addr:
                user.list.remove(product)
    return redirect(request.referrer)


if __name__ == "__main__":
    app.run(debug=True)
