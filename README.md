# 📖 Digital Occurrence Book System (DOBS)

A **Django Rest Framework (DRF)** powered API designed to digitize the traditional *Occurrence Book* used in security and law enforcement. The system allows secure logging, searching, and managing of incidents/occurrences, with support for **role-based access control**, **file uploads**, and **report exports**.

---

## 🚀 Features

- **User Authentication & Roles**
  - Custom user model (`Operator`, `Supervisor`, `Administrator`).
  - JWT authentication (login, refresh).
  - Role-based permissions using **Groups** and **DRF permissions**.

- **Occurrences Management**
  - CRUD endpoints for logging incidents.
  - File uploads (images, documents).
  - Filtering and search by date, type, or keywords.

- **Reports & Analytics**
  - Summary counts of incidents.
  - Time-series reporting of occurrences.
  - Export reports as **CSV** or **PDF**.
  - ⚠️ **Known Bug**: PDF export currently returns a document with fields but without populated data. This will be fixed in a future release.

- **Admin Panel**
  - Django admin with extended user model support.

---

## 🏗️ Tech Stack

- **Backend:** Django, Django REST Framework
- **Authentication:** JWT (SimpleJWT)
- **Database:** PostgreSQL (Render Managed DB)
- **Deployment:** Render Web Service
- **Testing:** Django Test Framework + Postman
- **Documentation:** DRF browsable API & Postman Collection

---

## ⚙️ Installation (Local Setup)

```bash
# Clone repo
git clone https://github.com/<your-username>/dobs.git
cd dobs

# Create & activate virtual environment
python -m venv venv
source venv/bin/activate   # on Mac/Linux
venv\Scripts\activate      # on Windows

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

DATABASE_NAME=dobs_project_db
DATABASE_USER=dobs_project_db_user
DATABASE_PASSWORD=yourpassword
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

---

## 🌐 Deployment (Render)

1. Push your project to GitHub.
2. Create a new **Web Service** on [Render](https://render.com).
3. Connect your repository.
4. Set **Build Command**:
   ```
   pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
   ```
5. Set **Start Command**:
   ```
   gunicorn dobs_project.wsgi
   ```
6. Add **Environment Variables** (same as `.env`).
7. Deploy 🚀

---

## 📡 API Endpoints

| Method | Endpoint                          | Description                     | Auth |
|--------|----------------------------------|---------------------------------|------|
| POST   | `/api/token/`                    | Obtain JWT token                | ❌   |
| POST   | `/api/token/refresh/`            | Refresh JWT token               | ❌   |
| GET    | `/api/occurrences/`              | List all occurrences            | ✅   |
| POST   | `/api/occurrences/`              | Create a new occurrence         | ✅   |
| GET    | `/api/occurrences/{id}/`         | Retrieve single occurrence      | ✅   |
| PATCH  | `/api/occurrences/{id}/`         | Update an occurrence            | ✅   |
| DELETE | `/api/occurrences/{id}/`         | Delete an occurrence            | ✅   |
| GET    | `/api/occurrences/?search=text`  | Search occurrences              | ✅   |
| GET    | `/api/reports/summary/`          | Summary stats                   | ✅   |
| GET    | `/api/reports/time-points/`      | Time-series of incidents        | ✅   |
| GET    | `/api/reports/export/pdf/`       | Export report as PDF (⚠️ bug: fields only, no data) | ✅   |
| GET    | `/api/reports/export/csv/`       | Export report as CSV            | ✅   |

---

## 🧪 Testing

Run Django tests:

```bash
python manage.py test
```

Or use **Postman** (Collection included below 👇).

---

## 📦 Postman Collection

A ready-to-import **Postman Collection** (`DOBS.postman_collection.json`) is provided to test:

- Authentication (login, refresh).
- CRUD on occurrences.
- File uploads.
- Filtering/search.
- Export endpoints (CSV & PDF).

📥 [Download Collection](./docs/DOBS.postman_collection.json)

---

## 📊 Example Workflow

1. **Login** → `/api/token/`
2. **Create occurrence** → `/api/occurrences/`
3. **Upload image** → `/api/occurrences/` (multipart form-data)
4. **Search** → `/api/occurrences/?search=gate`
5. **Export** → `/api/reports/export/pdf/`

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Thubelihle (Developer & Security Professional)**  
Built as part of the **ALX Backend Development Program**.
