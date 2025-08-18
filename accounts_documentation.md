# DOBS Project – Accounts App Documentation

## 1. Overview

The `accounts` app manages **user authentication, registration, and role-based access** in the Digital Occurrence Book System.

It includes:

- Custom user model (`User`) with roles
- JWT authentication for login
- Role-based access control for API endpoints

---

## 2. Models

### User

Custom user model extending `AbstractBaseUser` and `PermissionsMixin`.

| Field       | Type         | Description                                          |
| ----------- | ------------ | ---------------------------------------------------- |
| `username`  | CharField    | Unique username                                      |
| `email`     | EmailField   | Unique email address                                 |
| `role`      | CharField    | User role: `Operator`, `Supervisor`, `Administrator` |
| `is_active` | BooleanField | Is the user active?                                  |
| `is_staff`  | BooleanField | Is the user staff (required for admin login)?        |

**Custom Manager:** `CustomUserManager`

- `create_user(username, email, role, password)`
- `create_superuser(username, email, role='Administrator', password)`

---

## 3. Serializers

### UserRegistrationSerializer

Used for **creating new users**.

**Fields:**

- `username`
- `email`
- `role`
- `password` (write-only)
- `confirm_password` (write-only)

**Key Methods:**

- `validate`: Ensures `password` matches `confirm_password`
- `create`: Calls `CustomUserManager.create_user()`

### CustomTokenObtainPairSerializer

Used for **JWT login**.

**Features:**

- Extends `TokenObtainPairSerializer`
- Adds `role` to both the **JWT payload** and the **response**
- Returns:

```json
{
  "refresh": "<token>",
  "access": "<token>",
  "role": "Operator"
}
```

---

## 4. Views

| View                        | Type     | Purpose                     | Roles Allowed           |
| --------------------------- | -------- | --------------------------- | ----------------------- |
| `UserRegistrationView`      | APIView  | Register a new user         | Administrator only      |
| `CustomTokenObtainPairView` | JWT View | Obtain JWT tokens for login | All authenticated users |

**Notes:**

- `UserRegistrationView` uses **DRF permissions**: `IsAuthenticated + RoleRequiredMixin`
- RoleRequiredMixin ensures only Admins can register users.

---

## 5. URLs

| Endpoint              | Method | Description                    | Permissions |
| --------------------- | ------ | ------------------------------ | ----------- |
| `/accounts/register/` | POST   | Create a new user              | Admin only  |
| `/accounts/login/`    | POST   | Login and get JWT token + role | All users   |
| `/accounts/refresh/`  | POST   | Refresh JWT access token       | All users   |

**Request Examples:**

### Register (Admin only)

```json
POST /accounts/register/
Authorization: Bearer <admin_access_token>
{
  "username": "operator1",
  "email": "op1@example.com",
  "role": "Operator",
  "password": "StrongPass123",
  "confirm_password": "StrongPass123"
}
```

### Login

```json
POST /accounts/login/
{
  "username": "operator1",
  "password": "StrongPass123"
}
```

**Response:**

```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>",
  "role": "Operator"
}
```

---

## 6. Role-Based Access Control (RBAC)

| Role          | Permissions in Accounts App              |
| ------------- | ---------------------------------------- |
| Administrator | Can register users, login, refresh token |
| Operator      | Can login, refresh token                 |
| Supervisor    | Can login, refresh token                 |

> Other apps (Occurrences, Reports) enforce role-based access similarly.

---

## 7. Notes / Best Practices

1. **JWT Authentication**: All protected endpoints require `Authorization: Bearer <access_token>` header.
2. **Token Expiration**: Access tokens expire by default; use refresh tokens to obtain a new access token.
3. **Security**: Passwords are hashed automatically via `set_password`.

---

**End of Accounts App Documentation**

