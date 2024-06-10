
# Social Network API
## Features

- User signup
- User login with JWT authentication
- Search users by email or name
- Send, accept, and reject friend requests
- List friends
- List pending friend requests
- Rate limiting for friend requests (max 3 per minute)

## Requirements

- Python 3.8+
- Django 3.2+
- Django Rest Framework 3.12+
- Django Rest Framework SimpleJWT 4.7+

## Setup Instructions

Follow these steps to set up the project on your local machine:

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/social_network.git
cd social_network
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
# On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python manage.py migrate
```

### 5. Create a Superuser

```bash
python manage.py createsuperuser
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`.

## API Endpoints

### Authentication

- **Signup:** `POST /api/signup/`
  - Request Body: `{"email": "user@example.com", "username": "user", "password": "password123"}`
  
- **Login:** `POST /api/login/`
  - Request Body: `{"email": "user@example.com", "password": "password123"}`

### User Search

- **Search Users:** `GET /api/search/?q=keyword`
  - Query Params: `q` - search keyword (matches email or name)

### Friend Requests

- **Send Friend Request:** `POST /api/friend-requests/`
  - Request Body: `{"to_user": user_id}`
  
- **List Friend Requests:** `GET /api/friend-requests/`
  - Lists all friend requests sent and received by the authenticated user

- **Update Friend Request:** `PUT /api/friend-requests/<id>/`
  - Request Body: `{"status": "accepted"}` or `{"status": "rejected"}`

### Friends List

- **List Friends:** `GET /api/friends/`
  - Lists all friends of the authenticated user

### Pending Friend Requests

- **Pending Friend Requests:** `GET /api/pending-requests/`
  - Lists all pending friend requests received by the authenticated user

## Additional Configuration

### Settings

Ensure the following settings are included in your `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework_simplejwt',
    'api',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}
```
