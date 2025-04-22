# OTP Auth System 🔐

A Django-based authentication system with OTP (One-Time Password) verification, real-time email validation, and JWT-based login/logout functionality.

## 📌 Features

- ✅ User registration with email OTP verification
- ✅ Real-time email validation using Mailboxlayer API
- ✅ OTP expires in 10 minutes
- ✅ JWT-based authentication for login
- ✅ Secure logout with token blacklisting

---

## 📦 Technologies Used

- Python
- Django & Django REST Framework
- SimpleJWT (JWT Authentication)
- Mailboxlayer API (Real-time email validation)
- SQLite (for development)

---

## 🚀 API Endpoints

### 1. 📬 Register API

**Endpoint:** `/api/users/register/`  
**Method:** `POST`

Registers a new user and sends an OTP to their email for verification.

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "your_password",
  "full_name": "Rahul Chavda"
}
```

**Workflow:**
- Validates email using Mailboxlayer API.
- If valid, sends an OTP to the email (valid for 10 minutes).
- Temporarily stores user data in cache.
- On successful OTP verification, saves user data to the database.
- If OTP expires or verification fails, cached data is removed.

---

### 2. 🔑 Confirm OTP API

**Endpoint:** `/api/users/confirm-otp/`  
**Method:** `POST`

**Request Body:**

```json
{
  "email": "user@example.com",
  "otp": "123456"
}
```

- Confirms the OTP sent to the user.
- On success, creates and saves the user in the database.

---

### 3. 🔐 Login API

**Endpoint:** `/api/users/login/`  
**Method:** `POST`

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "your_password"
}
```

**Response:**

```json
{
  "access": "<access_token>",
  "refresh": "<refresh_token>"
}
```

- Verifies email and password.
- On success, returns JWT `access` and `refresh` tokens.

---

### 4. 🚪 Logout API

**Endpoint:** `/api/users/logout/`  
**Method:** `POST`

**Headers:**

```
Authorization: Bearer <access_token>
```

**Request Body:**

```json
{
  "refresh_token": "<refresh_token>"
}
```

- Blacklists the refresh token, making it unusable.
- Ensures the user is fully logged out.

---

## ⚙️ JWT Configuration (Sample)

```python
# settings.py
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

---

## 🧪 Testing

You can test the APIs using **Postman**:
- Register → Validate email via Mailboxlayer → Confirm OTP
- Login → Receive tokens
- Logout → Invalidate refresh token

---

## 📝 Notes

- OTP expires in 10 minutes.
- User data is cached until OTP is verified.
- Logout API uses token blacklisting to block access after logout.
- Mailboxlayer API must be properly configured in `.env` or `settings.py`.

---

## 📧 Contact

Created by **Chavda Rahul**. For questions or suggestions, feel free to connect!
