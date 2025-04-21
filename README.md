# OTP Auth System

A simple authentication system with **JWT-based login** and **OTP-based login**, plus **real-time email validation** using a third-party API. This ensures secure user authentication and prevents spam registrations.

## 🚀 Features

- **User Registration**: Users can sign up with an email and password.
- **JWT-based Login**: Secure login using JSON Web Tokens (JWT).
- **OTP-based Login**: Users can log in via OTP sent to their email.
- **OTP Expiry**: OTPs are valid only for a limited time (e.g., 5 minutes).
- **Secure Password Storage**: Passwords are hashed before storing them.
- **Real-time Email Validation**: Uses a third-party API to verify email deliverability before registration.
- **Resend OTP**: Option for users to request a new OTP if expired.

## 🛠️ Tech Stack

- **Backend**: Python (Django / Flask / FastAPI)
- **Authentication**: JWT (JSON Web Token), OTP (One-Time Password)
- **Database**: PostgreSQL / SQLite / MongoDB
- **Email Service**: SMTP or third-party (e.g., SendGrid, Mailgun)
- **Email Validation API**: Abstract API / ZeroBounce / Hunter.io / Kickbox

## 📋 Workflow

1. **User Registration**:
   - User provides name, email, and password.
   - System checks if the email is valid and deliverable using an external email validation API.
   - If valid, the password is hashed and user data is saved.

2. **JWT Login**:
   - User logs in with email and password.
   - On success, a JWT token is generated.

3. **OTP Login**:
   - User requests an OTP by entering their email.
   - If the email is registered, an OTP is generated and sent.
   - On correct OTP submission, a JWT token is issued.

4. **OTP Expiry**:
   - OTPs are valid for a limited time.
   - Expired OTPs require resending for a new attempt.

## 🚧 Installation

1. **Clone the repository**:
   ```cmd
   git clone https://github.com/your-username/OTP_auth_system.git
   cd OTP_auth_system
pip install -r requirements.txt
