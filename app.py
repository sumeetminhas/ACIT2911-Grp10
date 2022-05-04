from flask import Flask, render_template, request, redirect, url_for, flash
import os
import json

app = Flask(__name__)
app.secret_key = "sdfsanfdjksdbafkjsah"

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
    return render_template('about.html')

@app.route('/admin/dashboard', methods = ['POST'])
def dashboard():
    if request.method == 'POST':
        email, password = request.form['email'], request.form['password']
        with open('creds.json', 'r') as creds:
            admin_list = json.loads(creds.read())
            for admin in admin_list:
                if email == admin['email'] and password == admin['password']:
                    return render_template('admin_dashboard.html', user = admin['name'])
                else: 
                    flash("Incorrect email or password. Try Again..")
                    print('What the fuck is happening?')
                    return redirect('/admin')

# @app.route('/add_user')
# def add_user():
#     if request.method in ['POST', 'GET']:
#         name = request.form['user_name']
#         email = request.form['email']
#         password = request.form['password']
#         with open('creds.json', 'r') as creds:
#             admin_list = json.loads(creds.read())
#             new_admin = {
#                 "name": name,
#                 "email": email,
#                 "password": password
#             }
#             admin_list.append(new_admin)
#             with open('creds.json', 'w') as file:
#                 file.write(json.dumps(admin_list))
#             return "Success"
#     else: 
#         return "Not working"

if __name__ == "__main__":
    app.run(debug=True)