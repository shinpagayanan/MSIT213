**Shane Corporate Asset Tracker**

Corporate Asset Tracker is a web-based system designed to help organizations efficiently manage, monitor, and track company assets. The system uses role-based access control to ensure users have appropriate permissions based on their responsibilities. It improves accountability, transparency, and operational efficiency in handling company resources.

**Features:**
  Asset registration and management
  Employee asset assignment tracking
  Asset Maintenance Tracking
  Record keeping and reporting
  Search and filter functionality
  Role-based access control
'

**User Roles and Credentials**

**Super Admin:**

  Full system access
  Manage users (add, edit, delete)
  Manage all assets (Create, Edit, Delete)
  Print Reports

  Login Credentials:
    Username: admin
    Password: 123

**Manager or Administrator:**

  Register Users
  Manage all assets (Create, Edit, Delete)
  Print Reports

  Login Credentials:
    Username: jane
    Password: Jane12345

**Employee**

  View asset list
  Print Reports
  
  Login Credentials: 
    Username: john
    Password: John12345


**Installation Guide**

1. Create a virtual environment:
python -m venv .venv

2. Activate the virtual environment:
Windows: .venv\Scripts\activate
Mac/Linux: source .venv/bin/activate

3. Install dependencies:
pip install -r requirements.txt

4. Run the server:
python manage.py runserver

5. Open in browser:
http://127.0.0.1:8000/
