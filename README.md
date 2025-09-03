# 🛡️ Django Rate Limiting & Suspicious IP Tracking

A Django-based project that provides **rate limiting** for user
authentication endpoints and tracks **suspicious IP addresses** using
Celery tasks. The system is designed to prevent brute-force login
attempts, block malicious IPs, and monitor abnormal request activity.

------------------------------------------------------------------------

## ✨ Features

-   🚦 **Dynamic rate limiting** for authenticated vs anonymous users\
-   📌 **Redis-backed cache** for consistent rate limiting across
    workers\
-   📝 **Request logging** with IP, path, timestamp, country & city\
-   🔒 **Blocked IP model** to prevent repeated offenders from accessing
    the app\
-   🔎 **Suspicious IP tracking** with configurable rules:
    -   More than 100 requests/hour
    -   Accessing sensitive endpoints (e.g., `/login`, `/admin`)\
-   ⏰ **Hourly Celery task** to analyze IP activity\
-   🗄️ **Django ORM models** for persistence and auditing\
-   🐳 **Redis integration** for caching and task brokering

------------------------------------------------------------------------

## 🛠️ Tech Stack

-   **Django** (Backend framework)\
-   **Django Ratelimit** (Rate limiting)\
-   **Celery** (Task queue)\
-   **Redis** (Broker, result backend, and cache)\
-   **SQLite** (Database --- or any Django-supported DB)

------------------------------------------------------------------------

## ⚙️ Setup & Installation

### 1. Clone the Repository

``` bash
git clone https://github.com/loutimi/alx-backend-security.git
cd alx-backend-security
```

### 2. Create & Activate Virtual Environment

``` bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies

``` bash
pip install -r requirements.txt
```

### 4. Configure Redis

Make sure Redis is installed and running locally:

``` bash
redis-server
```

### 5. Configure Django Settings

Update `settings.py`:

``` python
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",  # DB 1 for cache
    }
}

RATELIMIT_USE_CACHE = "default"

CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"   # DB 0 for Celery
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"
```

### 6. Run Database Migrations

``` bash
python manage.py migrate
```

### 7. Start Services

Run Django server:

``` bash
python manage.py runserver
```

Run Celery worker:

``` bash
celery -A alx-backend-security worker -l info
```

Run Celery beat (for scheduled tasks):

``` bash
celery -A alx-backend-security beat -l info
```

------------------------------------------------------------------------

## 📂 Project Structure

    alx-backend-security/
    │── ip_tracking/
    │   ├── models.py        # RequestLog, BlockedIP, SuspiciousIP models
    │   ├── tasks.py         # Celery task to analyze IP activity
    │   ├── views.py         # Login view with rate limiting
    │   ├── middleware.py    # Logs requests with geolocation
    │
    │── alx-backend-security/
    │   ├── celery.py        # Celery app setup
    │   ├── settings.py      # Django + Redis + Ratelimit config
    │
    ├── requirements.txt
    ├── manage.py

------------------------------------------------------------------------

## 📊 Models

### RequestLog

  -------------------------------------------------------------------------
  Field        Type                Description
  ------------ ------------------- ----------------------------------------
  ip_address   GenericIPAddress    IP of the client making the request

  timestamp    DateTime (auto_add) When the request was made

  path         CharField           The endpoint accessed

  country      CharField           Resolved country from IP (if available)
               (nullable)          

  city         CharField           Resolved city from IP (if available)
               (nullable)          
  -------------------------------------------------------------------------

### BlockedIP

  -------------------------------------------------------------------------
  Field        Type                Description
  ------------ ------------------- ----------------------------------------
  ip_address   GenericIPAddress    Permanently blocked IP address

  -------------------------------------------------------------------------

### SuspiciousIP

  -------------------------------------------------------------------------
  Field        Type                Description
  ------------ ------------------- ----------------------------------------
  ip_address   GenericIPAddress    The IP flagged as suspicious

  reason       CharField           Reason for flagging

  timestamp    DateTime (auto_add) When the IP was flagged
  -------------------------------------------------------------------------

------------------------------------------------------------------------

## 🚀 Usage

-   Anonymous users → limited to **5 requests/minute**\
-   Authenticated users → limited to **10 requests/minute**\
-   Every incoming request is logged with IP, path, timestamp, and
    location (if resolved)\
-   Every hour, Celery runs a task to:
    -   Check request logs
    -   Flag IPs exceeding **100 requests/hour**
    -   Flag IPs accessing sensitive paths (`/login`, `/admin`)
    -   Store flagged IPs in `SuspiciousIP`
    -   Optionally, add repeated offenders to `BlockedIP`

------------------------------------------------------------------------

## 📜 License

MIT License. Free to use and modify.

------------------------------------------------------------------------

## 👨‍💻 Author

**Rotimi Musa**\
Backend Developer \| Data Enthusiast
