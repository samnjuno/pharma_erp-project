# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from models import User


# Initialize the app
app = Flask(__name__)

# Set up the database URI (using SQLite for simplicity)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pharma_erp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'mysecretkey'  # Replace with a strong secret key

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
migrate = Migrate(app, db)

# Import models after initializing db to avoid circular imports
from models import User, Product, Supplier, Sale, PurchaseOrder

# Route to test app
@app.route('/')
def index():
    return 'Pharma ERP System Running!'

if __name__ == '__main__':
    app.run(debug=True)
    
 
# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:  # Password should be hashed in real-world apps
            login_user(user)
            return redirect(url_for('dashboard'))

        flash('Login Unsuccessful. Check username and password.', 'danger')

    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Dashboard route (protected)
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

