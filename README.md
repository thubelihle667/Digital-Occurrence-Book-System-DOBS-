# DOBS – Digital Occurrence Book System (Capstone Project)

## 📌 Project Overview
The **Digital Occurrence Book System (DOBS)** is a web-based API built with **Django Rest Framework (DRF)**.  
It is designed to replace traditional paper-based occurrence books used in security, policing, and control room environments.  

The system allows operators to:
- Log incidents (occurrences) in real time.  
- Manage users with role-based access (Operator, Supervisor, Administrator).  
- Upload evidence such as images.  
- Search, filter, and organize records for quick retrieval.  
- Secure the platform with authentication, permissions, and API best practices.  

---

## 🛠️ Tech Stack
- **Backend:** Django, Django REST Framework  
- **Database:** SQLite (for development)  
- **Auth:** JWT Authentication (SimpleJWT)  
- **Security:** CSRF, Django security middleware, DRF permissions  
- **Testing:** Django Test Framework & DRF test client  
- **Deployment-ready:** Compatible with Nginx/Apache setups  

---

## 👥 User Roles
- **Operator** → Create and view occurrences they log.  
- **Supervisor** → Review, edit, and filter occurrences across the system.  
- **Administrator** → Full system access, including managing users and permissions.  

---

## 🔑 Authentication
- JWT-based authentication (using **SimpleJWT**).  
- Endpoints for login, logout, and token refresh.  
- Users must authenticate to access most resources.  

---

## 📂 Apps Breakdown
### 1. **Accounts App**
- Custom user model (with `date_of_birth`, `profile_photo`, and `role`).  
- Endpoints for registration, login, logout.  
- JWT integration for authentication.  

### 2. **Occurrences App**
- Core app for managing incident records.  
- Fields: `title`, `description`, `category`, `location`, `date_reported`, `status`, `reported_by`.  
- Supports image/file uploads.  
- Role-based access control.  

### 3. **Reports App**
- Generate structured reports based on filters (e.g., date, category).  
- Export-ready endpoints (future scope).  

### 4. **Posts (Social Media-style Updates)**
- Allow users to share quick updates, with comment support.  
- Linked to user authentication.  

---

## 🔍 Search & Filtering
Implemented **DRF filters + full-text search**:  
- **Search fields:** `title`, `description`, `location`, `category`.  
- **Filter fields:** `date_reported`, `status`, `category`.  
- Example query:  
  ```http
  GET /api/occurrences/?search=theft&category=Crime&date_reported=2025-08-01
  ```

---

## 🔐 Security Settings
- CSRF protection enabled for browsable API.  
- Secure headers applied via Django middleware:
  - `X-Content-Type-Options: nosniff`  
  - `X-Frame-Options: DENY`  
  - `SECURE_BROWSER_XSS_FILTER`  
- HTTPS-ready configuration for deployment.  
- Permissions enforced at endpoint level (Operators can’t see all logs, Admins can).  

---

## 🧪 Testing & Demo
- Unit tests for models, serializers, views, and permissions.  
- API tests using `APITestCase` with JWT authentication.  
- Tested CRUD operations for all endpoints.  
- Final demo will be presented using **Postman** to showcase endpoints in action.  

---

## 📌 API Endpoints

### 🔒 Accounts
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/accounts/register/` | Register new user |
| POST | `/api/accounts/login/` | Login & obtain JWT |
| POST | `/api/accounts/logout/` | Logout user |
| POST | `/api/accounts/token/refresh/` | Refresh JWT |

#### Example: Register User
**Request**
```http
POST /api/accounts/register/
Content-Type: application/json

{
  "username": "alice",
  "password": "pass1234",
  "role": "Operator",
  "date_of_birth": "1999-05-10"
}
```
**Response**
```json
{
  "id": 1,
  "username": "alice",
  "role": "Operator",
  "date_of_birth": "1999-05-10"
}
```

---

### 📝 Occurrences
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/occurrences/` | List all occurrences (with search & filters) |
| POST | `/api/occurrences/` | Create new occurrence |
| GET | `/api/occurrences/{id}/` | Retrieve occurrence by ID |
| PUT/PATCH | `/api/occurrences/{id}/` | Update occurrence |
| DELETE | `/api/occurrences/{id}/` | Delete occurrence (admin/supervisor only) |

#### Example: Create Occurrence
**Request**
```http
POST /api/occurrences/
Authorization: Bearer <your_token>
Content-Type: application/json

{
  "title": "Unauthorized Access",
  "description": "Suspicious individual entered restricted area",
  "category": "Security",
  "location": "Gate 3",
  "status": "Open"
}
```
**Response**
```json
{
  "id": 5,
  "title": "Unauthorized Access",
  "description": "Suspicious individual entered restricted area",
  "category": "Security",
  "location": "Gate 3",
  "status": "Open",
  "reported_by": "alice",
  "date_reported": "2025-08-27T19:20:30Z"
}
```

---

### 📊 Reports
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/reports/` | List all reports |
| GET | `/api/reports/?date=2025-08-20` | Filter reports by date |
| GET | `/api/reports/?category=Accident` | Filter by category |

#### Example: Fetch Reports by Category
**Request**
```http
GET /api/reports/?category=Accident
Authorization: Bearer <your_token>
```
**Response**
```json
[
  {
    "id": 2,
    "title": "Car Accident",
    "category": "Accident",
    "location": "Main Road",
    "date_reported": "2025-08-20T14:22:00Z",
    "status": "Closed"
  }
]
```

---

### 💬 Posts
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/posts/` | List posts |
| POST | `/api/posts/` | Create post |
| GET | `/api/posts/{id}/` | Retrieve post |
| POST | `/api/posts/{id}/comments/` | Add comment to post |

#### Example: Add Comment
**Request**
```http
POST /api/posts/1/comments/
Authorization: Bearer <your_token>
Content-Type: application/json

{
  "text": "Great work on resolving this issue quickly!"
}
```
**Response**
```json
{
  "id": 3,
  "post": 1,
  "text": "Great work on resolving this issue quickly!",
  "author": "supervisor1",
  "created_at": "2025-08-27T18:55:00Z"
}
```

---

## 🚀 How to Run Locally
1. Clone repo:
   ```bash
   git clone https://github.com/yourusername/DOBS.git
   cd DOBS
   ```
2. Setup environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/Mac
   .venv\Scripts\activate      # Windows
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```
5. Start server:
   ```bash
   python manage.py runserver
   ```

---

## 🌍 Deployment Notes
- Works with **Gunicorn + Nginx** or **Apache mod_wsgi**.  
- Update settings for:
  - `ALLOWED_HOSTS`  
  - `SECURE_SSL_REDIRECT = True` (for HTTPS)  
  - Database configs (PostgreSQL recommended for production).  

---

## 🎯 Final Notes
The **DOBS Capstone Project** demonstrates beginner-to-intermediate Django + DRF skills, with added polish in:  
- **Search & filtering** for usability.  
- **Security settings** for production readiness.  
- **Thorough testing** for stability.  
- **Presentation-ready API demo** (via Postman).  

---
