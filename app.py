from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diet_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model for diet logs
class DietLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meal = db.Column(db.String(100), nullable=False)
    calories = db.Column(db.Integer, nullable=False)

# Workaround to create tables only once using before_request
@app.before_request
def create_tables():
    if not hasattr(app, 'tables_created'):
        db.create_all()
        app.tables_created = True

# Route: Home page
@app.route('/')
def home():
    return render_template('home.html')

# Route: Registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Here you would handle registration logic
        return redirect(url_for('home'))
    return render_template('register.html')

# Route: Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Here you would handle login logic
        return redirect(url_for('home'))
    return render_template('login.html')

# Route: Diet log page
@app.route('/diet-log')
def diet_log():
    logs = DietLog.query.all()
    return render_template('diet_log.html', logs=logs)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
