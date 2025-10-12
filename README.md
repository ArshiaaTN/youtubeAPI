# 🎬 Video Subscription Platform API

A comprehensive Django REST API for a video streaming platform with subscription-based access control, user authentication, video interactions, and complete history tracking.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Database Models](#database-models)
- [Authentication](#authentication)
- [Subscription Tiers](#subscription-tiers)
- [Usage Examples](#usage-examples)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project is a fully-featured video subscription platform backend built with Django and Django REST Framework. It provides a complete solution for managing video content, user subscriptions, payment processing, and user interactions with videos.

The platform implements a Netflix-like subscription model where users can purchase different subscription tiers to access video content at varying quality levels. It includes a virtual wallet system for payments, comprehensive video interaction features (likes, comments), and detailed history tracking for both video watching and payment transactions.

## ✨ Features

### 🔐 Authentication & Authorization
- **JWT-based Authentication** - Secure token-based authentication using access and refresh tokens
- **User Registration** - New users can sign up with username, email, and password
- **User Login/Logout** - Secure login with JWT token generation and token blacklisting on logout
- **Profile Management** - Users can view and update their profile information
- **Password Update** - Secure password change functionality
- **Role-Based Access Control** - Separate permissions for regular users and administrators

### 💳 Wallet System
- **Virtual Wallet** - Each user has a digital wallet with balance tracking
- **Wallet Charging** - Users can add funds to their wallet (simulated payment)
- **Balance Inquiry** - Check current wallet balance at any time
- **Transaction History** - Complete record of all wallet transactions
- **Automatic Deduction** - Subscription purchases automatically deduct from wallet balance

### 📺 Subscription Management
- **Three Subscription Tiers**
  - **Basic** (100,000 Toman) - 480p video quality
  - **Premium** (250,000 Toman) - 720p video quality
  - **VIP** (500,000 Toman) - 1080p video quality
- **Subscription Purchase** - Buy subscriptions using wallet balance
- **Subscription Renewal** - Upgrade or renew existing subscriptions
- **Auto-deactivation** - Previous subscriptions automatically deactivated on renewal
- **Subscription History** - View all past and current subscriptions
- **Access Control** - Video access restricted based on active subscription status

### 🎥 Video Management
- **Admin Video CRUD** - Administrators can create, read, update, and delete videos
- **Video Listing** - Browse all available videos with metadata
- **Video Details** - View comprehensive information about each video
- **View Counter** - Automatic tracking of video views
- **Quality-Based Streaming** - Video quality served based on user's subscription tier

### 👍 Video Interactions
- **Like System** - Users can like videos (one like per user per video)
- **Unlike Functionality** - Remove likes from previously liked videos
- **Comment System** - Add text comments to videos
- **Comment Display** - View all comments with username and timestamp
- **Video Statistics** - Real-time stats showing views, likes, and comment counts
- **User Like Status** - API indicates if current user has liked a video

### 📊 History Tracking
- **Watch History** - Complete record of all videos watched by user
- **Watch Duration Tracking** - Store how long each video was watched
- **Payment History** - Detailed log of all subscription payments
- **Combined History View** - Single endpoint to view both watch and payment history
- **Date-Based Sorting** - History sorted by most recent first

## 🛠️ Tech Stack

- **Backend Framework:** Django 5.2.7
- **API Framework:** Django REST Framework 3.15.2
- **Authentication:** djangorestframework-simplejwt 5.3.1
- **Database:** SQLite3 (Development) / PostgreSQL-ready (Production)
- **Python Version:** 3.12.6
- **API Architecture:** RESTful API
- **Authentication Method:** JWT (JSON Web Tokens)

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.12 or higher** - [Download Python](https://www.python.org/downloads/)
- **pip** - Python package installer (included with Python)
- **Git** - [Download Git](https://git-scm.com/downloads)
- **Virtual Environment** - Recommended for isolated dependency management

## 🚀 Installation

Follow these steps to set up the project locally:

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/youtubeAPI.git
cd youtubeAPI
```

### 2. Create Virtual Environment

**On Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration (Optional)

Create a `.env` file in the root directory for environment variables:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Database Setup

Run migrations to create database tables:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Admin User

Create a superuser account to access admin features:

```bash
python manage.py createsuperuser
```

Follow the prompts to set:
- Username
- Email address
- Password

### 7. Run Development Server

Start the Django development server:

```bash
python manage.py runserver
```

The API will be accessible at: **http://127.0.0.1:8000/**

Admin panel: **http://127.0.0.1:8000/admin/**


### Using Postman Collection

We've included a Postman collection for easy API testing:

1. **Import Collection:**
   - Open Postman
   - Click **Import**
   - Select `postman/youtubeAPI.postman_collection.json`

## 📚 API Documentation

### Base URL
```
http://127.0.0.1:8000/api/
```

### API Endpoints Overview

#### Authentication Endpoints
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/signup/` | Register new user | No |
| POST | `/auth/login/` | User login | No |
| POST | `/auth/logout/` | User logout | Yes |
| POST | `/auth/token/refresh/` | Refresh access token | No |
| GET | `/auth/profile/` | Get user profile | Yes |
| PUT | `/auth/profile/` | Update user profile | Yes |

#### Wallet Endpoints
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/auth/wallet/` | Check wallet balance | Yes |
| POST | `/auth/wallet/` | Charge wallet | Yes |

#### Video Management Endpoints
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/videos/` | List all videos | Yes |
| POST | `/videos/` | Create video (Admin) | Yes (Admin) |
| GET | `/videos/<id>/` | Get video details | Yes |
| PUT | `/videos/<id>/` | Update video (Admin) | Yes (Admin) |
| DELETE | `/videos/<id>/` | Delete video (Admin) | Yes (Admin) |

#### Video Interaction Endpoints
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/videos/<id>/watch/` | Watch video | Yes |
| POST | `/videos/<id>/like/` | Like video | Yes |
| DELETE | `/videos/<id>/like/` | Unlike video | Yes |
| GET | `/videos/<id>/comments/` | Get comments | Yes |
| POST | `/videos/<id>/comments/` | Add comment | Yes |
| GET | `/videos/<id>/stats/` | Get video statistics | Yes |

#### Subscription Endpoints
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/subscriptions/` | Get active subscription | Yes |
| POST | `/subscriptions/` | Purchase subscription | Yes |
| DELETE | `/subscriptions/` | Cancel subscription | Yes |
| POST | `/subscriptions/renew/` | Renew subscription | Yes |
| GET | `/subscriptions/history/` | Subscription history | Yes |

#### History Endpoints
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/history/watch/` | Watch history | Yes |
| GET | `/history/payment/` | Payment history | Yes |
| GET | `/history/all/` | Combined history | Yes |

### Detailed API Examples

#### 1. User Registration
```http
POST /api/auth/signup/
Content-Type: application/json

{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123"
}
```

**Response (201 Created):**
```json
{
    "message": "User created successfully",
    "user": {
        "username": "john_doe",
        "email": "john@example.com"
    }
}
```

#### 2. User Login
```http
POST /api/auth/login/
Content-Type: application/json

{
    "username": "john_doe",
    "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
    "message": "User logged in successfully",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "username": "john_doe"
}
```

#### 3. Charge Wallet
```http
POST /api/auth/wallet/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "amount": 500000
}
```

**Response (200 OK):**
```json
{
    "message": "Wallet charged successfully with 500000",
    "new_balance": "500000.00"
}
```

#### 4. Purchase Subscription
```http
POST /api/subscriptions/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "type": "Premium"
}
```

**Response (201 Created):**
```json
{
    "message": "Subscription purchased successfully",
    "subscription": {
        "id": 1,
        "type": "Premium",
        "start_date": "2025-10-11",
        "end_date": "2025-11-10",
        "price": 250000,
        "is_active": true
    },
    "remaining_balance": "250000.00"
}
```

#### 5. Watch Video
```http
POST /api/videos/1/watch/
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
    "message": "Video is now playing",
    "video": {
        "id": 1,
        "title": "Introduction to Django",
        "description": "Learn Django basics",
        "video_url": "https://example.com/video.mp4",
        "quality": "720p",
        "duration": "01:30:00"
    },
    "subscription_type": "Premium"
}
```

#### 6. Like Video
```http
POST /api/videos/1/like/
Authorization: Bearer <access_token>
```

**Response (201 Created):**
```json
{
    "message": "Video liked successfully",
    "likes_count": 26
}
```

#### 7. Add Comment
```http
POST /api/videos/1/comments/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "text": "Great tutorial! Very helpful."
}
```

**Response (201 Created):**
```json
{
    "message": "Comment added successfully",
    "comment": {
        "id": 1,
        "username": "john_doe",
        "text": "Great tutorial! Very helpful.",
        "created_at": "2025-10-11T14:30:00Z"
    }
}
```

## 📁 Project Structure

```
youtubeAPI/
│
├── accounts/                    # User authentication & profile management
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py               # Custom User model with wallet
│   ├── serializers.py          # User & wallet serializers
│   ├── tests.py
│   ├── urls.py
│   └── views.py                # Auth endpoints (signup, login, profile)
│
├── videos/                      # Video management & interactions
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py               # Video, Like, Comment models
│   ├── serializers.py          # Video-related serializers
│   ├── tests.py
│   ├── urls.py
│   └── views.py                # Video CRUD & interaction endpoints
│
├── subscriptions/               # Subscription management
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py               # Subscription model
│   ├── serializers.py          # Subscription serializers
│   ├── tests.py
│   ├── urls.py
│   └── views.py                # Subscription endpoints
│
├── payments/                    # Payment processing
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py               # Payment model
│   ├── tests.py
│   └── views.py
│
├── history/                     # Watch & payment history
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py               # History model
│   ├── serializers.py          # History serializers
│   ├── tests.py
│   ├── urls.py
│   └── views.py                # History endpoints
│
├── youtubeAPI/                  # Project configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py             # Django settings
│   ├── urls.py                 # Main URL configuration
│   └── wsgi.py
│
├── .gitignore                   # Git ignore file
├── db.sqlite3                   # SQLite database
├── manage.py                    # Django management script
├── README.md                    # This file
└── requirements.txt             # Python dependencies
```

## 🔐 Authentication

This API uses **JWT (JSON Web Tokens)** for authentication.

### Token Types

1. **Access Token**
   - Short-lived (5 minutes)
   - Used for API authentication
   - Include in Authorization header

2. **Refresh Token**
   - Long-lived (1 day)
   - Used to obtain new access tokens
   - Should be stored securely

### Using Tokens

Include the access token in the Authorization header of your requests:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Token Refresh

When your access token expires, use the refresh token to get a new one:

```http
POST /api/auth/token/refresh/
Content-Type: application/json

{
    "refresh": "your_refresh_token_here"
}
```

### Token Expiration

- **Access tokens expire after 5 minutes** for security
- **Refresh tokens expire after 1 day**
- Implement automatic token refresh in your client application

## 💎 Subscription Tiers

| Tier | Price (Toman) | Video Quality | Features |
|------|---------------|---------------|----------|
| **Basic** | 100,000 | 480p | • Access to all videos<br>• Standard definition<br>• Like & comment features |
| **Premium** | 250,000 | 720p | • All Basic features<br>• High definition (HD)<br>• Better viewing experience |
| **VIP** | 500,000 | 1080p | • All Premium features<br>• Full HD quality<br>• Best viewing experience |

### Subscription Rules

- **Duration:** All subscriptions are valid for 30 days
- **Active Status:** Only one active subscription allowed per user
- **Renewal:** Renewing creates a new subscription and deactivates the old one
- **Access Control:** Must have active subscription to watch videos
- **Quality:** Video quality automatically served based on subscription tier

## 💡 Usage Examples

### Complete User Journey

```bash
# 1. Register a new user
curl -X POST http://127.0.0.1:8000/api/auth/signup/ \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","email":"alice@example.com","password":"alice123"}'

# 2. Login to get tokens
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"alice123"}'

# 3. Check wallet balance
curl -X GET http://127.0.0.1:8000/api/auth/wallet/ \
  -H "Authorization: Bearer <access_token>"

# 4. Charge wallet
curl -X POST http://127.0.0.1:8000/api/auth/wallet/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"amount":500000}'

# 5. Purchase subscription
curl -X POST http://127.0.0.1:8000/api/subscriptions/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"type":"Premium"}'

# 6. List available videos
curl -X GET http://127.0.0.1:8000/api/videos/ \
  -H "Authorization: Bearer <access_token>"

# 7. Watch a video
curl -X POST http://127.0.0.1:8000/api/videos/1/watch/ \
  -H "Authorization: Bearer <access_token>"

# 8. Like the video
curl -X POST http://127.0.0.1:8000/api/videos/1/like/ \
  -H "Authorization: Bearer <access_token>"

# 9. Add a comment
curl -X POST http://127.0.0.1:8000/api/videos/1/comments/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"text":"Great video!"}'

# 10. Check watch history
curl -X GET http://127.0.0.1:8000/api/history/watch/ \
  -H "Authorization: Bearer <access_token>"
```

## 🧪 Testing

### Using Postman

1. **Import Collection**
   - Create a new collection in Postman
   - Add all API endpoints

2. **Set Environment Variables**
   ```
   base_url: http://127.0.0.1:8000
   access_token: <your_access_token>
   refresh_token: <your_refresh_token>
   ```

3. **Test Workflow**
   - Sign up → Login → Charge Wallet → Purchase Subscription → Watch Video

### Manual Testing with curl

See [Usage Examples](#usage-examples) section for curl commands.

### Automated Testing

Run Django tests:

```bash
python manage.py test
```


## 📄 License

This project is created for educational purposes as part of a Django bootcamp. Feel free to use it for learning and personal projects.

## 👨‍💻 Author

**Arshia TN**
- GitHub: [@ArshiaaTN](https://github.com/ArshiaaTN)

**Made with ❤️ using Django and Django REST Framework**