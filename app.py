from email.message import Message
from unicodedata import name
from flask import Flask, render_template, request, redirect, url_for, flash, session
from cart import Cart
import os
import json
import csv
from functions import read_products, read_json, add_to_history, class_to_dict, update_products
from werkzeug.utils import secure_filename
import datetime
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = "super-secret-key"

"""Mail Server Settings"""
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'ostopshop10@gmail.com'
app.config['MAIL_PASSWORD'] = 'Acit@2911'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

LIVE_SESSIONS = []
active_cart = []

products_file_path = os.path.join(app.root_path, 'admin-only')
login_file_path = os.path.join(app.root_path, 'admin-only', 'creds.json')
transactions_file_path = os.path.join(app.root_path, 'admin-only', 'transactions.json')

PRODUCT_LIST, IMAGES = read_products()
TRANSACTIONS = read_json()

"""Mail Server Settings"""
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'ostopshop10@gmail.com'
app.config['MAIL_PASSWORD'] = 'Acit@2911'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

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
    if os.path.exists(os.path.join(products_file_path, 'products.csv')):
        return render_template('/products.html', products=PRODUCT_LIST, image_list=IMAGES, users=LIVE_SESSIONS)
    else:
        return "<h1>No Products to display</h1><h2>Please visit us at a later time.</h2>"



@app.route('/admin', methods=["GET"])
def admin():
    if request.method == "GET":
        if os.path.exists(login_file_path):
            with open(login_file_path, 'r') as creds:
                admin_list = json.load(creds)
                print(session.values())
                for admin in admin_list:
                    print(admin['email'])
                    if admin['email'] in session.values():
                        return redirect('/admin/dashboard')
                
                return render_template('admin-login.html')
    else:
        return '<h1>Admin Portal not set up. Please use static features. '


@app.route('/admin/dashboard', methods=['POST', 'GET'])
def dashboard():
    if request.method == 'POST':
        with open(login_file_path, 'r') as creds:
            admin_list = json.load(creds)
            email, password = request.form['email'], request.form['password']
            for admin in admin_list:
                if admin['email'] in session.values(): 
                    return render_template('admin_dashboard.html', user=admin['name'], products=PRODUCT_LIST, history=TRANSACTIONS[::-1])
                elif email == admin['email'] and password == admin['password']:
                    session["email"] = email
                    return render_template('admin_dashboard.html', user=admin['name'], products=PRODUCT_LIST, history=TRANSACTIONS[::-1])
            flash("Incorrect email or password. Try Again..")
            return redirect('/admin')

    elif request.method == 'GET':
        with open(login_file_path, 'r') as creds:
            admin_list = json.load(creds)
            for admin in admin_list:
                if admin['email'] in session.values():
                    return render_template('admin_dashboard.html', user=admin['name'], products=PRODUCT_LIST, history=TRANSACTIONS[::-1])

            return redirect('/admin')

@app.route('/sign_out', methods=["GET"])
def sign_out():
    if request.method == "GET":
        with open(login_file_path, 'r') as creds:
            admin_list = json.load(creds)
            for admin in admin_list:
                if admin['email'] in session.values():
                    session.clear()
                    return redirect('admin')
                
    return redirect(url_for('admin'))

@app.route('/about')
def about():
    for user in LIVE_SESSIONS:
        if user.owner == request.remote_addr:
            for item in user.list:
                print(item)
    return render_template('about.html', users=LIVE_SESSIONS)


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
                user + product
                user.update_total(float(product[2][1:]))

                for item in PRODUCT_LIST:
                    if item[1] == product[1]:
                        item[5] = int(item[5]) - 1
                update_products(PRODUCT_LIST)
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
                user - product
                user.update_total(float(product[2][1:]) * -1)
            
                for item in PRODUCT_LIST:
                    if item[1] == product[1]:
                        item[5] = int(item[5]) + 1
                update_products(PRODUCT_LIST)

    return redirect(request.referrer)

@app.route('/update-inventory', methods = ["GET", "POST"])
def update_inventory():
    if request.method == 'POST':
        with open(os.path.join(products_file_path, 'products.csv'), 'r') as file:
            file = request.files['file-name']
            file.save(os.path.join(products_file_path, secure_filename('products.csv')))
            print(file)

        return redirect(request.referrer)

@app.route('/checkout', methods=["POST", "GET"])
def checkout():
    if request.method == "POST":
        return render_template('checkout.html', product=TRANSACTIONS, users=LIVE_SESSIONS)
    else:
        return redirect('/')


@app.route('/confirm-checkout', methods=['POST'])
def email():
    if request.method == "POST":
        full_name = request.form["full-name"]
        email = request.form["email"]
        phone_num = request.form["phone-num"]
        addr_st = request.form["address-st"]
        addr_city = request.form["address-city"]
        addr_coun = request.form["address-country"]
        addr_code = request.form["address-code"]
        address = f"{addr_st}, {addr_city}, {addr_coun}, {addr_code}"
        for user in LIVE_SESSIONS:
            if user.owner == request.remote_addr:
                comp_cart, cart_total = class_to_dict(user)
                user.clear_cart()
        
        msg = Message(f"Order invoice: {full_name}",
        sender='ostopshop10@gmail.com',
        recipients=[email])

        msg.html = f"""
            <p>Email: {email}</p>
            <p>Phone No: {phone_num}</p>
            <p>Address: {address}</p>
            {comp_cart}
            <br>
            <p>Amount for Cart: {cart_total}</p>
            <p>Taxes: {cart_total*0.12}</p>
            <h3>Total amount: {cart_total * 1.12 }</h3>
        """
        mail.send(msg)

        trans_summary = {
            "name": full_name,
            "email": email,
            "address": address,
            "Product_list": comp_cart,
            "Order-total": cart_total,
            "date": datetime.datetime.now().strftime("%c")
        }

        add_to_history(trans_summary, TRANSACTIONS)

        return """
        <h2>Order has been placed</h2>
        <a href="/">Return to Homepage</a>
        """
    
    else: 
        return redirect('/')
    

if __name__ == "__main__":
    app.run(debug=True)
