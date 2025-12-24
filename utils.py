import json
import os
from datetime import datetime
import glob
from werkzeug.utils import secure_filename

DATA_DIR = 'data_submissions'

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def save_submission(service_name, form_data):
    """
    Data save karta hai. 
    Agar Leave form hai to naam: ID_Type_Date.json hoga.
    """
    service_folder = os.path.join(DATA_DIR, service_name)
    if not os.path.exists(service_folder):
        os.makedirs(service_folder)
    
    # 1. Basic Data Extraction
    emp_id = form_data.get('emp_id', 'UNKNOWN').strip()
    # Windows filename mein '/' mana hai, isliye agar ID mein '/' hai to '-' kar do
    emp_id = secure_filename(emp_id) 
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 2. Custom Naming Logic based on Service
    if service_name == 'leave':
        # Leave Type nikalo (Annual, Sick etc.)
        leave_type = form_data.get('leave_type', 'Request')
        # Application Date nikalo
        app_date = form_data.get('app_date', datetime.now().strftime("%Y-%m-%d"))
        
        # File Name: E4095_Annual_2025-12-14.json
        filename = f"{emp_id}_{leave_type}_{app_date}.json"
        
    elif service_name == 'salary_adv':
        app_date = form_data.get('app_date', datetime.now().strftime("%Y-%m-%d"))
        filename = f"{emp_id}_SalaryAdv_{app_date}.json"
        
    else:
        # Default Logic for other forms
        filename = f"{emp_id}_{timestamp}.json"
    
    # 3. Save File
    # Agar filename mein spaces hain to underscores bana do taake error na aaye
    filename = filename.replace(' ', '_').replace('/', '-')
    
    filepath = os.path.join(service_folder, filename)
    
    with open(filepath, 'w') as f:
        json.dump(form_data, f, indent=4)
        
    return True

# --- Baaki Functions Same Rahenge ---
def load_stats():
    # ... (Purana code same rakhein) ...
    if not os.path.exists('service_stats.json'):
        return {'total': 0}
    try:
        with open('service_stats.json', 'r') as f:
            return json.load(f)
    except:
        return {}

def increment_count(service_name):
    # ... (Purana code same rakhein) ...
    stats = load_stats()
    stats[service_name] = stats.get(service_name, 0) + 1
    stats['total'] = stats.get('total', 0) + 1
    with open('service_stats.json', 'w') as f:
        json.dump(stats, f)

def get_service_stats():
    # ... (Purana code same rakhein) ...
    stats = {'total': 0}
    services = ['leave', 'salary_adv', 'it_access', 'no_dues', 'contract', 'salary_cert', 'passport']
    for service in services:
        folder = os.path.join(DATA_DIR, service)
        count = 0
        if os.path.exists(folder):
            count = len(glob.glob(os.path.join(folder, "*.json")))
        stats[service] = count
        stats['total'] += count
    return stats

def get_all_requests(service_name):
    # ... (Purana code same rakhein) ...
    folder = os.path.join(DATA_DIR, service_name)
    requests = []
    if os.path.exists(folder):
        files = glob.glob(os.path.join(folder, "*.json"))
        files.sort(key=os.path.getmtime, reverse=True)
        for file in files:
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                    requests.append({
                        'filename': os.path.basename(file),
                        'emp_id': data.get('emp_id', 'N/A'),
                        'emp_name': data.get('emp_name', 'N/A'),
                        'date': data.get('app_date', 'N/A') # Ab Date file ke andar se aayegi
                    })
            except: continue
    return requests

def load_submission_data(service_name, filename):
    # ... (Purana code same rakhein) ...
    filepath = os.path.join(DATA_DIR, service_name, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return {}