from flask import Flask, redirect, url_for
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.forms import forms_bp
from routes.employee_data import employee_bp

app = Flask(__name__)
app.secret_key = "pan_home_secure_key_2025"

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(forms_bp)
app.register_blueprint(employee_bp)

@app.route('/')
def index():
    # Yahan change kiya hai: 'auth.login_page' ki jagah 'auth.login'
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True)