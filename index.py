from flask import Flask, render_template_string, request, redirect, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# In-memory user store for demonstration purposes
users = {'user@example.com': {'password': 'password'}}

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Login template
login_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
        form { display: inline-block; text-align: left; }
        label, input { display: block; margin: 10px 0; }
    </style>
</head>
<body>
    <h1>Login</h1>
    <form method="post" action="/login">
        <label>Email:</label>
        <input type="text" name="email">
        <label>Password:</label>
        <input type="password" name="password">
        <input type="submit" value="Login">
    </form>
    <p>Don't have an account? <a href="/signup">Sign up here</a></p>
</body>
</html>
"""

# Sign-up template
signup_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Sign Up</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
        form { display: inline-block; text-align: left; }
        label, input { display: block; margin: 10px 0; }
    </style>
</head>
<body>
    <h1>Sign Up</h1>
    <form method="post" action="/signup">
        <label>Email:</label>
        <input type="text" name="email">
        <label>Password:</label>
        <input type="password" name="password">
        <input type="submit" value="Sign Up">
    </form>
</body>
</html>
"""

# Home template with Google Maps
home_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Home - BBC Ev Charging App</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
        form { display: inline-block; text-align: left; }
        label, select, input { display: block; margin: 10px 0; }
        #map { height: 400px; width: 100%; margin-top: 20px; }
    </style>
    <script>
        function initMap() {
            var mapOptions = {
                center: {lat: 37.7749, lng: -122.4194}, // Default to San Francisco, change as needed
                zoom: 10
            };
            var map = new google.maps.Map(document.getElementById('map'), mapOptions);
        }
    </script>
</head>
<body>
    <h1>Welcome to the BBC Ev Charging App</h1>
    {% if current_user.is_authenticated %}
        <p>Hello, {{ current_user.id }}!</p>
        {% if session.selected_car %}
            <p>You have chosen: {{ session.selected_car }}</p>
        {% endif %}
        <p><a href="/step2">Start App</a></p>
        <p><a href="/logout">Logout</a></p>
        <div id="map"></div>
    {% else %}
        <p>Please <a href="/login">login</a> or <a href="/signup">sign up</a> to continue.</p>
    {% endif %}
    <script async defer src="https://maps.googleapis.com/maps/api/js?key=YOUR_GOOGLE_MAPS_API_KEY&callback=initMap"></script>
</body>
</html>
"""

# Library template
library_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Car Library</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
        form { display: inline-block; text-align: left; }
        label, select, input { display: block; margin: 10px 0; }
    </style>
</head>
<body>
    <h2>Here is the car library:</h2>
    <form method="post" action="/choose_car">
        <label>Type the car you would like to choose:</label>
        <select name="car_choice">
            <option value="Tesla">Tesla</option>
            <option value="BMW">BMW</option>
            <option value="Mercedes">Mercedes</option>
            <option value="Other">Other</option>
        </select>
        <input type="submit" value="Submit">
    </form>
</body>
</html>
"""

# Bluetooth template
bluetooth_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Bluetooth Scan</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
        form { display: inline-block; text-align: left; }
        label, select, input { display: block; margin: 10px 0; }
    </style>
</head>
<body>
    <h2>Scanning for Car...</h2>
    <form method="post" action="/bluetooth_choice">
        <label>Would you like to connect to the device?</label>
        <select name="connect">
            <option value="Y">Yes</option>
            <option value="N">No</option>
        </select>
        <input type="submit" value="Submit">
    </form>
</body>
</html>
"""

# Car choice template
car_choice_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Car Choice</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
    </style>
</head>
<body>
    <h2>You have chosen the {{ car_choice }}</h2>
</body>
</html>
"""

# Use device template
use_device_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Use Device</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
        form { display: inline-block; text-align: left; }
        label, select, input { display: block; margin: 10px 0; }
    </style>
</head>
<body>
    <h2>Connecting to the device...</h2>
    <form method="post" action="/use_device_choice">
        <label>Would you like to use the device?</label>
        <select name="use">
            <option value="Y">Yes</option>
            <option value="N">No</option>
        </select>
        <input type="submit" value="Submit">
    </form>
</body>
</html>
"""

# Result template
result_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Result</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
    </style>
</head>
<body>
    <h2>{{ message }}</h2>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    return render_template_string(home_template)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if email in users and users[email]['password'] == password:
            user = User(email)
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash("Invalid credentials", "error")
    return render_template_string(login_template)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if email in users:
            flash("User already exists!", "error")
        else:
            users[email] = {'password': password}
            user = User(email)
            login_user(user)
            return redirect(url_for('index'))
    return render_template_string(signup_template)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/step2", methods=["GET", "POST"])
@login_required
def step2():
    if request.method == "POST":
        choice = request.form.get("choice")
        if choice == "L":
            return render_template_string(library_template)
        elif choice == "B":
            return render_template_string(bluetooth_template)
        else:
            return "Error, wrong value. Please restart the program."
    return render_template_string(home_template)

@app.route("/choose_car", methods=["POST"])
@login_required
def choose_car():
    car_choice = request.form.get("car_choice")
    car_choices = {
        "Tesla": [
            "Tesla Model 3", "Tesla Model S", "Tesla Model X", "Tesla Model Y", 
            "Tesla Model 3 Plus", "Tesla Model S Plus", "Tesla Model X Plus", 
            "Tesla Model Y Plus", "Tesla Model 3 Plus Hybrid", 
            "Tesla Model S Plus Hybrid", "Tesla Model X Plus Hybrid", 
            "Tesla Model Y Plus Hybrid", "Tesla Model 3 Electric", 
            "Tesla Model S Electric", "Tesla Model X Electric", "Tesla Model Y Electric"
        ],
        "BMW": [
            "BMW i3", "BMW i8", "BMW iX", "BMW iX3", "BMW iX4", "BMW iX5", "BMW iX6", 
            "BMW iX7", "BMW iX8", "BMW iX3 M", "BMW iX4 M", "BMW iX5 M", "BMW iX6 M", 
            "BMW iX7 M", "BMW iX8 M", "BMW iX3 M Sport"
        ],
        "Mercedes": [
            "Mercedes-Benz C-Class", "Mercedes-Benz E-Class", "Mercedes-Benz G-Class", 
            "Mercedes-Benz S-Class"
        ],
        "Other": []
    }
    if car_choice in car_choices:
        options = ''.join([f'<option value="{car}">{car}</option>' for car in car_choices[car_choice]])
        car_choice_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Choose Car Model</title>
            <style>
                body {{ font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }}
                form {{ display: inline-block; text-align: left; }}
                label, select, input {{ display: block; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <h2>You chose {car_choice}</h2>
            <form method="post" action="/confirm_car">
                <label>Type the number of the car you would like to choose:</label>
                <select name="car_model">
                    {options}
                </select>
                <input type="submit" value="Submit">
            </form>
        </body>
        </html>
        """
        return render_template_string(car_choice_html, car_choice=car_choice)
    else:
        return render_template_string(result_template, message=f"Your car is a {car_choice}")

@app.route("/confirm_car", methods=["POST"])
@login_required
def confirm_car():
    car_model = request.form.get("car_model")
    session['selected_car'] = car_model
    return redirect(url_for('index'))

@app.route("/bluetooth_choice", methods=["POST"])
@login_required
def bluetooth_choice():
    connect = request.form.get("connect")
    if connect == "Y":
        return render_template_string(use_device_template)
    else:
        return render_template_string(result_template, message="Device is now not used.")

@app.route("/use_device_choice", methods=["POST"])
@login_required
def use_device_choice():
    use = request.form.get("use")
    if use == "Y":
        return render_template_string(result_template, message="Using the device... Device is now used.")
    else:
        return render_template_string(result_template, message="Device is now not used.")

if __name__ == "__main__":
    app.run(debug=True)
