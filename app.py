from flask import Flask, render_template, request, redirect, url_for
import os
import json

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('/home.html')

@app.route('/products')
def products():
    return render_template('/products.html')

@app.route('/admin')
def admin():
    return render_template('admin-login.html')

@app.route('/about')
def about():
    return redirect

@app.route('/admin/dashboard', methods = ['POST'])
def dashboard():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        with open('creds.json', 'r') as creds:
            admin_list = json.loads(creds.read())
            for admin in admin_list:
                print(password, email)
                if email == admin['email'] and password == admin['password']:
                    return render_template('admin_dashboard.html', user = admin['name'])
                else: return "Failure to authenticate"

if __name__ == "__main__":
    app.run(debug=True)