# DOBS Project

## Project Overview
The **Digital Occurrence Book System (DOBS)** is a Django REST Framework project designed to streamline security reporting and monitoring for organizations. The system allows operators, supervisors, and administrators to manage occurrences and reports efficiently.

---

## Key Features

### 1. User Authentication & Roles
- Custom user model with roles: **Operator**, **Supervisor**, **Administrator**
- JWT-based authentication for secure login and token management
- Role-based access control (RBAC) for all API endpoints

### 2. Occurrences Management
- Operators can create new occurrence records
- Supervisors and Administrators can view and monitor occurrences
- Each occurrence includes details such as title, description, location, and timestamp

### 3. Reports & Monitoring
- Supervisors and Administrators can generate and view reports based on occurrences
- Ensures accountability and oversight for security operations

### 4. API Endpoints
- **Accounts:** `/accounts/register/`, `/accounts/login/`, `/accounts/refresh/`
- **Occurrences:** `/occurrences/create/`, `/occurrences/list/`, `/occurrences/<id>/`
- **Reports:** `/reports/list/`

### 5. Security & Best Practices
- Passwords are securely hashed using Django's built-in methods
- Access tokens expire and can be refreshed using JWT refresh tokens
- Role-based permissions ensure users only access authorized endpoints

### 6. Tech Stack
- **Backend:** Django, Django REST Framework
- **Authentication:** JWT (via `djangorestframework-simplejwt`)
- **Database:** PostgreSQL (recommended)
- **Testing:** Postman collection provided for API testing

---

## Getting Started
1. Clone the repository
2. Set up a virtual environment and install dependencies (`pip install -r requirements.txt`)
3. Configure your PostgreSQL database in `settings.py`
4. Apply migrations (`python manage.py migrate`)
5. Create a superuser for administrative access (`python manage.py createsuperuser`)
6. Run the server (`python manage.py runserver`)
7. Use Postman to test API endpoints with JWT authentication

---

## Notes
- Admin users can register other users
- Operator users can only create occurrences
- Supervisor users can view occurrences and reports
- Ensure to include JWT access token in the `Authorization` header for protected endpoints

---

**End of README**

