from flask import Flask, render_template, request, redirect, url_for, flash, session
from cart import Cart
import os
import json
import csv

app = Flask(__name__)
app.secret_key = "sdfsanfdjksdbafkjsah"

LIVE_SESSIONS = []


@app.route('/')
def homepage():
    if len(LIVE_SESSIONS) == 0:
        LIVE_SESSIONS.append(Cart(request.remote_addr))
    for user in LIVE_SESSIONS:
        if user.owner == request.remote_addr:
            break
        else: LIVE_SESSIONS.append(Cart(request.remote_addr))
    return render_template('/home.html', users=LIVE_SESSIONS)


@app.route('/products')
def products():
    if os.path.exists('products.csv'):
        with open('products.csv', 'r') as file:
            product_list = list(csv.reader(file))
            images = os.listdir('static/product_image')
            new_list = []
            for image in images:
                new_list.append(image[:-4])
            # print(images[0])
            # print(product_list[1])
            # print(new_list[0])

        return render_template('/products.html', products=product_list, image_list=new_list)
    else:
        return "<h1>No Products to display</h1><h2>Please visit us at a later time.</h2>"



@app.route('/admin')
def admin():
    with open('creds.json', 'r') as creds:
            admin_list = json.loads(creds.read())
            for admin in admin_list:
                if admin['email'] in session.values():
                    return render_template('admin_dashboard.html', user=admin['name'])
            return render_template('admin-login.html')


@app.route('/about')
def about():
    print(LIVE_SESSIONS)
    return render_template('about.html')


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



if __name__ == "__main__":
    app.run(debug=True)
