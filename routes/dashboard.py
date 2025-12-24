from flask import Blueprint, render_template, session, redirect, url_for
from utils import get_service_stats, get_all_requests

dashboard_bp = Blueprint('dashboard', __name__)

# --- CONFIGURATION: Folder Name vs Route Function Name ---
SERVICE_MAP = {
    'leave': 'forms.leave_application',
    'salary_adv': 'forms.salary_advance',
    'it_access': 'forms.it_access',
    'no_dues': 'forms.no_dues',
    'contract': 'forms.contract_amendment',
    'salary_cert': 'forms.salary_cert',
    'passport': 'forms.passport_request'
}

@dashboard_bp.route('/dashboard')
def home():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    current_stats = get_service_stats()
    return render_template('dashboard.html', user=session['user'], stats=current_stats)

@dashboard_bp.route('/requests/<service_name>')
def request_list(service_name):
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    # 1. Get List of Files
    req_list = get_all_requests(service_name)
    
    # 2. Get Title
    title = service_name.replace('_', ' ').title()
    
    # 3. Get Correct Endpoint for View/Edit
    # Agar service map mein nahi mili to wapis dashboard bhej do
    target_endpoint = SERVICE_MAP.get(service_name)
    
    if not target_endpoint:
        return "Error: Service Route Not Found"

    return render_template('requests_list.html', 
                           requests=req_list, 
                           title=title, 
                           endpoint=target_endpoint) # <-- Endpoint pass kar rahe hain