from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register')
def register():
    return "User registration page"

@app.route('/login')
def login():
    return "Login page"

@app.route('/diet-log')
def diet_log():
    return "Your Diet Log"

if __name__ == '__main__':
    app.run(debug=True)
