from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from forms import RegistrationForm, LoginForm
from forms import HomeForm


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
    form = HomeForm()  # Ensure HomeForm is properly imported
    if form.validate_on_submit():
        flash('Form submitted successfully!', 'success')
        return redirect(url_for('home'))  # Redirect after POST to avoid re-submission
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
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/diet-log')
@login_required
def diet_log():
    logs = DietLog.query.all()
    return render_template('diet_log.html', logs=logs)

@app.route('/logout')
def logout():
    logout_user()  # This will log out the user
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
