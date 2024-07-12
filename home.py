from flask import Flask, render_template_string, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Mock user store (replace with your actual user management)
users = {'user@example.com': {'password': 'password'}}

# User class for Flask-Login (replace with your actual User model)
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Login template (unchanged)
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

# Sign-up template (unchanged)
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

# Home template
home_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Home - BBC Ev Charging App</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
        form { display: inline-block; text-align: left; }
        label, select, input { display: block; margin: 10px 0; }
    </style>
</head>
<body>
    <h1>Welcome to the BBC Ev Charging App</h1>
    <p>Please <a href="/login">login</a> or <a href="/signup">sign up</a> to continue.</p>
</body>
</html>
"""

# Routes

@app.route("/")
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
            return redirect(url_for('home'))
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
            return redirect(url_for('home'))
    return render_template_string(signup_template)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))  # Redirect to home page

# Your existing routes for the BBC Ev Charging App

if __name__ == "__main__":
    app.run(debug=True)
