from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('/home.html')

@app.route('/products')
def products():
    return '<h1>Products Page</h1>'

@app.route('/admin')
def admin():
    return '<h1>Admin Login Page</h1>'

@app.route('/about')
def about():
    return '<h1>About our One Stop Shop</h1>'

if __name__ == "__main__":
    app.run(debug=True)