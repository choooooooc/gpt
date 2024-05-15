from flask import Flask, request, render_template, redirect, url_for, flash
from flask import session
from functools import wraps
from forms import RegistrationForm, LoginForm
from config import Config
from flask_sqlalchemy import SQLAlchemy
from openai import OpenAI
import json
import logging

app = Flask (__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Load configuration for OpenAI
with open("openai_config.json") as config_file:
    config = json.load(config_file)

# Logger setup for debugging
logging.basicConfig(level=logging.INFO)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in or register to continue.', 'info')
            return redirect(url_for('welcome'))
        return f(*args, **kwargs)
    return decorated_function


class User(db.Model):
    """
    User model representing a user record in the database.

    Attributes:
        id (int): The primary key.
        name (str): The user's name.
        age (int): The user's age.
        email (str): The user's email address.
        weight (float): The user's weight.
        height (float): The user's height.
        body_fat_percentage (float): The user's body fat percentage.
        bmi (float): The user's calculated BMI.
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    body_fat_percentage = db.Column(db.Float, nullable=False)
    bmi = db.Column(db.Float, nullable=True)
    def __init__(self, name, age, email, weight, height, body_fat_percentage):
        self.name = name
        self.email = email
        self.age = age
        self.weight = float(weight)
        self.height = float(height)
        self.body_fat_percentage = body_fat_percentage
        self.bmi = self.weight / ((self.height / 100) ** 2)

@app.route('/')
@login_required
def index():
    """
    Route for the homepage that displays the latest user information.
    Requires the user to be logged in. Redirects to logout route if no user is found.
    """
    
    user_id = session.get('username')
    user = User.query.filter_by(name=user_id).order_by(User.id.desc()).first() 
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('logout'))
    return render_template('index.html', user=user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Route for registering a new user. If accessed via GET, it displays the
    registration form. If accessed via POST with valid form data, it creates
    a new user record in the database and redirects to the login page.
    """
    form = RegistrationForm()
    if request.method == 'GET':
        return render_template('register_form.html', form=form)
    elif request.method == 'POST':
        if True:
            print('printing form data')
            user = User(
                request.form['username'],
                request.form['age'],
                request.form['email'],
                request.form['weight'],
                request.form['height'],
                request.form['bodyfat']
            )
            db.session.add(user)
            db.session.commit() 
        return render_template('register_submitted.html')



def query_openai(prompt):
    """
    Sends a prompt to the OpenAI API and retrieves the generated response.

    Args:
        prompt (str): The prompt string to send for processing.

    Returns:
        str: The response message from OpenAI API.
    """
    client = OpenAI(base_url=config["base_url"], api_key=config["base_url"])
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message
    except Exception as e:
        logging.error(f'OpenAI query failed: {e}')
        return None
    
@app.route("/results", methods=['GET', 'POST'])
def results():
    user_id = request.form.get('user_id')
    user = User.query.get(user_id)
   
    user.health_goals = request.form.get("plan")
    user.target_weight=request.form.get("target weight")
    user.duration=request.form.get("duration")
    
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('index'))
    prompt = f"{user.name} has a BMI of {user.bmi:.1f}, a body fat of {user.body_fat_percentage} and is looking to {user.health_goals}. His/ Her current weight is {user.weight} kg, and his/her target weight is {user.target_weight} kg, he/she want to complete this in {user.duration}. Can you suggest a {user.health_goals} plan? please response in the format: 1. how many carlories can you get today. 2. what's your suggested diet today. 3. what's your ideal workout today."
        
    plan = query_openai(prompt)
    response = plan.content
    response = response.replace("\n", "<br>")
    print(response)
    return render_template('results.html', user=user, response=response)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        if user:
            session['user_id'] = user.id
            session['username'] = user.name
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username.', 'error')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.clear()  # Clear the entire session
    flash('You have been logged out.', 'success')
    return redirect(url_for('welcome'))

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


if __name__ == '__main__':
    with app.app_context():
        #db.drop_all()
        db.create_all()
        app.run(debug=True)