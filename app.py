from flask import Flask, render_template, request, redirect

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
        
        return f"<h1>Admin Dashboard: Authorization still pending</h1><h2>{email}</h2>"

if __name__ == "__main__":
    app.run(debug=True)