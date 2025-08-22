# 📝 Django Occurrence Book System (DOBS)

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-ff1709?style=for-the-badge&logo=django&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=jsonwebtokens)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![ALX](https://img.shields.io/badge/ALX-DC143C?style=for-the-badge&logo=academia&logoColor=white)

The **Django Occurrence Book System (DOBS)** is a digital record-keeping
platform inspired by traditional security and law enforcement
*occurrence books*.\
It allows authorized users to log, manage, and review incidents in a
structured and secure way.\
This project is being developed as part of the **ALX Back-End Web
Development Capstone Project**.

------------------------------------------------------------------------

## 🚀 Features

### ✅ Implemented

-   **User Authentication & Accounts (accounts app)**
    -   Custom user model extending Django's `AbstractUser`
    -   User registration, login, and logout via API endpoints
    -   JWT-based authentication with `djangorestframework-simplejwt`
    -   Role and permission management for controlled access
-   **Occurrence Management (occurrences app)**
    -   Create, view, update, and delete occurrence records
    -   API endpoints for managing incidents
    -   Each occurrence linked to the reporting user
    -   Support for timestamped logging of incidents

------------------------------------------------------------------------

### 🔜 Planned (Future Enhancements)

-   **Reports app** -- generate and export structured reports (PDF/CSV)\
-   **Occurrence comments** -- allow users to discuss or add notes to
    records\
-   **User activity logs** -- track logins, updates, and sensitive
    actions\
-   **Deployment** -- Nginx/Apache setup for production use with
    PostgreSQL database

------------------------------------------------------------------------

## 🛠️ Tech Stack

-   **Backend:** Django, Django REST Framework (DRF)\
-   **Authentication:** JWT (SimpleJWT)\
-   **Database:** SQLite (development), PostgreSQL (recommended for
    production)\
-   **Deployment:** Gunicorn + Nginx/Apache (planned)

------------------------------------------------------------------------

## 📂 Project Structure

    dobs_project/
    │── accounts/         # User authentication & management
    │── occurrences/      # Occurrence (incident) logging system
    │── dob_project/      # Core settings and configurations
    │── manage.py

------------------------------------------------------------------------

## 📌 API Endpoints (current)

### Accounts

-   `POST /api/accounts/register/` → Register new user\
-   `POST /api/accounts/login/` → User login, returns JWT token\
-   `POST /api/accounts/logout/` → User logout

### Occurrences

-   `GET /api/occurrences/` → List all occurrences\
-   `POST /api/occurrences/` → Create new occurrence\
-   `GET /api/occurrences/{id}/` → Retrieve single occurrence\
-   `PUT /api/occurrences/{id}/` → Update occurrence\
-   `DELETE /api/occurrences/{id}/` → Delete occurrence

------------------------------------------------------------------------

## ⚙️ Installation & Setup

1.  **Clone the repository**

    ``` bash
    git clone https://github.com/yourusername/DOBS.git
    cd DOBS
    ```

2.  **Create a virtual environment & install dependencies**

    ``` bash
    python -m venv venv
    source venv/bin/activate   # Linux/Mac
    venv\Scripts\activate      # Windows

    pip install -r requirements.txt
    ```

3.  **Configure environment variables**

    -   Copy `.env.example` → `.env`
    -   Update database, secret key, and JWT settings

4.  **Run migrations**

    ``` bash
    python manage.py migrate
    ```

5.  **Start development server**

    ``` bash
    python manage.py runserver
    ```

------------------------------------------------------------------------

## 📖 Usage

-   Use **Postman** or **cURL** to test API endpoints\
-   Authenticate using JWT tokens to access protected routes\
-   Admin panel available at `/admin/` (superuser required)

------------------------------------------------------------------------

## 🤝 Contributing

Contributions are welcome!\
1. Fork the repo\
2. Create a new branch (`git checkout -b feature-branch`)\
3. Commit your changes (`git commit -m 'Add new feature'`)\
4. Push to the branch (`git push origin feature-branch`)\
5. Open a Pull Request

------------------------------------------------------------------------

## 👤 Author

**Thubelihle Ngcobo**\
CCTV Operator \| Aspiring Back-End Developer\
Built as part of the **ALX Backend Development Program**
