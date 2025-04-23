# OTP Auth System 🔐

A Django-based authentication system with OTP (One-Time Password) verification, real-time email validation, and JWT-based login/logout and password reset functionality.

## 📌 Features

- ✅ User registration with email OTP verification
- ✅ Real-time email validation using Mailboxlayer API
- ✅ OTP expires in 10 minutes
- ✅ JWT-based authentication for login
- ✅ Secure logout with token blacklisting
- ✅ Reset password with jwt token

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
### 5. Forgot Password API
**Endpoint:** `api/users/forgot-password/`
**Method:** POST

Allows user to request a password reset by email. If the user exists, a secure JWT reset token is generated.

**Request Body:**
```JSON
{
  "email": "user@example.com"
}
```

**Response:**
```JSON
{
  "reset_token": "<jwt_reset_token>"
}
```
 - Always returns a generic success message for security (whether the user exists or not).

 - The reset token is valid for 10–15 minutes.

 - Can be used in the next step to reset the password.
---

---
### 6. Reset Password API
**Endpoint:** `/api/users/reset-password/`
**Method:** `POST`  

**Request Body:** 
```JSON
{
  "token": "<jwt_reset_token>",
  "new_password": "<New Password>"
}
```

**Response:**
```JSON
{
  {"message": "Password has been successfully reset."}
}

{
  "message": "Invalid or expired reset token."
}

{
  "message": "Reset token is required."
}

'''
- Return Success message for the successful reset of the password.
- JWT token is blacklist.
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
- Forgot Password → Receive JWT token → Use token to reset password

---

## 📝 Notes

- OTP expires in 10 minutes.
- User data is cached until OTP is verified.
- Logout API uses token blacklisting to block access after logout.
- Mailboxlayer API must be properly configured in `.env` or `settings.py`.

---

## 📧 Contact

Created by **Chavda Rahul**. For questions or suggestions, feel free to connect!
