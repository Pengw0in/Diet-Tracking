from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from forms import RegistrationForm, LoginForm
from forms import HomeForm
from flask import flash, redirect, url_for


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Use a strong, random key in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # SQLite for development

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirect users to login page if not logged in

# Define user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

# Diet log model
class DietLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meal = db.Column(db.String(100), nullable=False)
    calories = db.Column(db.Integer, nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/', methods=['GET', 'POST'])
def home():
    form = HomeForm()
    if form.validate_on_submit():
        # Process the email or save it as necessary
        flash('Email submitted successfully!', 'success')
        return redirect(url_for('diet_log'))  # Redirect to the diet log page (or any other page)
    return render_template('home.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            flash(f"Welcome, {user.username}!", "success")
            return redirect(url_for('dashboard'))  # Change 'dashboard' to your actual route name
        else:
            flash("Invalid username or password. Please try again.", "danger")
    return render_template('login.html', form=form)

from flask_login import login_required

@app.route('/diet-log')
@login_required  # Ensures the user is logged in
def diet_log():
    logs = DietLog.query.all()
    return render_template('diet_log.html', logs=logs)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out!', 'info')
    return redirect(url_for('home'))  # Redirect to home after logging out

@app.route('/test')
def test():
    return 'Test page works!'


if __name__ == '__main__':
    app.run(debug=True)
