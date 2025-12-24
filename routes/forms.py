from flask import Blueprint, render_template, session, redirect, url_for, request
from utils import save_submission, load_submission_data

forms_bp = Blueprint('forms', __name__)

def check_login():
    if 'user' not in session: return False
    return True

# Generic Handler
def handle_form(template_name, service_name):
    if not check_login(): return redirect(url_for('auth.login'))
    
    # SAVE DATA
    if request.method == 'POST':
        form_data = request.form.to_dict()
        save_submission(service_name, form_data)
        # Save hone ke baad wapis list par bhej do
        return redirect(url_for('dashboard.request_list', service_name=service_name))

    # LOAD DATA (Edit)
    file_name = request.args.get('file')
    existing_data = {}
    if file_name:
        existing_data = load_submission_data(service_name, file_name)

    return render_template(template_name, user=session['user'], data=existing_data)

# --- Routes ---

@forms_bp.route('/forms/leave-application', methods=['GET', 'POST'])
def leave_application():
    return handle_form('forms/leave.html', 'leave')

# ... (Baaki routes same rahenge bas methods=['GET', 'POST'] zaroor ho) ...
@forms_bp.route('/forms/salary-advance', methods=['GET', 'POST'])
def salary_advance():
    return handle_form('forms/salary_adv.html', 'salary_adv')

@forms_bp.route('/forms/it-access', methods=['GET', 'POST'])
def it_access():
    return handle_form('forms/it_access.html', 'it_access')

@forms_bp.route('/forms/no-dues', methods=['GET', 'POST'])
def no_dues():
    return handle_form('forms/no_dues.html', 'no_dues')

@forms_bp.route('/forms/contract-amendment', methods=['GET', 'POST'])
def contract_amendment():
    return handle_form('forms/contract_amendment.html', 'contract')

@forms_bp.route('/forms/salary-cert', methods=['GET', 'POST'])
def salary_cert():
    return handle_form('forms/salary_cert.html', 'salary_cert')

@forms_bp.route('/forms/passport-request', methods=['GET', 'POST'])
def passport_request():
    return handle_form('forms/passport_request.html', 'passport')

@forms_bp.route('/forms/on-duty')
def on_duty():
    return "<h1>On Duty Slip Coming Soon</h1>"