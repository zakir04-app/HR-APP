from flask import Blueprint, render_template, request, redirect, url_for, session

auth_bp = Blueprint('auth', __name__)

# Ek hi route jo GET (Page show) aur POST (Login check) dono karega
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # 1. Agar User Page Khol Raha Hai (GET Request)
    if request.method == 'GET':
        # Agar pehlay se login hai to Dashboard bhej do
        if 'user' in session:
            return redirect(url_for('dashboard.home'))
        return render_template('login.html')

    # 2. Agar User Login Button Daba Raha Hai (POST Request)
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check ID/Pass
        if username.lower() == "admin" and password == "admin123":
            session['user'] = "Admin"
            return redirect(url_for('dashboard.home'))
        else:
            return render_template('login.html', error="Invalid Username or Password")

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('auth.login'))