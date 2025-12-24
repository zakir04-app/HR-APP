import os
import pandas as pd
from flask import Blueprint, request, render_template, jsonify

employee_bp = Blueprint('employee', __name__)

# Data Folder Setup
DATA_FOLDER = 'data'
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

MASTER_DB_PATH = os.path.join(DATA_FOLDER, 'master_employees.csv')

# --- 1. Upload Route (Smart File Detection) ---
@employee_bp.route('/upload-data', methods=['GET', 'POST'])
def upload_data():
    msg = None
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"
        
        file = request.files['file']
        if file.filename == '':
            return "No selected file"

        try:
            # STEP 1: Smart Read (Try CSV first, then Excel)
            try:
                # Pehlay CSV samajh kar padhne ki koshish karein
                df = pd.read_csv(file, encoding='utf-8')
            except:
                # Agar fail ho jaye (kyunki file asal mein Excel hai), to Excel reader use karein
                file.seek(0) # File ko shuru se dubara padhein
                df = pd.read_excel(file)

            # STEP 2: Column Names Cleaning (Taake spelling mistake se code na phate)
            # Saare columns ke spaces khatam karein (e.g., "Employee No" -> "EmployeeNo")
            df.columns = [c.strip().replace(" ", "") for c in df.columns]
            
            # Column mapping check (Headers match karne ke liye)
            # Agar file mein 'ID' likha hai to hum usay 'EmployeeNo' samjhenge
            rename_map = {
                'EmpID': 'EmployeeNo', 'ID': 'EmployeeNo', 'EmployeeNumber': 'EmployeeNo',
                'Designation': 'Position', 'JobTitle': 'Position',
                'JoiningDate': 'DateOfJoining', 'DOJ': 'DateOfJoining'
            }
            df.rename(columns=rename_map, inplace=True)

            # STEP 3: Save as clean Master CSV
            df.to_csv(MASTER_DB_PATH, index=False)
            msg = f"Success! {len(df)} employees loaded securely."

        except Exception as e:
            msg = f"Error: File format not recognized. ({str(e)})"

    return render_template('upload_data.html', msg=msg)

# --- 2. Search API (For Auto-Fill) ---
@employee_bp.route('/get-employee/<emp_id>')
def get_employee_details(emp_id):
    if not os.path.exists(MASTER_DB_PATH):
        return jsonify({'found': False, 'error': 'Database missing.'})

    # ID ko clean karein (spaces hatayein aur uppercase karein)
    emp_id = str(emp_id).strip().upper()
    
    try:
        df = pd.read_csv(MASTER_DB_PATH)
        
        # Ensure EmployeeNo column is treated as String
        df['EmployeeNo'] = df['EmployeeNo'].astype(str).str.strip().str.upper()
        
        # Search for ID
        record = df[df['EmployeeNo'] == emp_id]

        if not record.empty:
            row = record.iloc[0].fillna('')
            return jsonify({
                'found': True,
                'name': str(row.get('Name', '')),
                'position': str(row.get('Position', '')),
                'department': str(row.get('Department', '')),
                'location': str(row.get('Location', '')),
                'joining_date': str(row.get('DateOfJoining', '')),
                'grade': str(row.get('Grade', ''))
            })
        else:
            return jsonify({'found': False})

    except Exception as e:
        print(f"Search Error: {e}")
        return jsonify({'found': False})