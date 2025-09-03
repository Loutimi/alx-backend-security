# 🛡️ Django Rate Limiting & Suspicious IP Tracking

A robust Django-based security system that provides **intelligent rate limiting** for authentication endpoints and **automated suspicious IP tracking** using Celery background tasks. Designed to prevent brute-force attacks, block malicious IPs, and monitor abnormal request patterns in real-time.

## ✨ Key Features

- **🚦 Dynamic Rate Limiting**
  - Authenticated users: 10 requests/minute
  - Anonymous users: 5 requests/minute
  - Redis-backed for consistency across multiple workers

- **📊 Comprehensive Request Monitoring**
  - Real-time IP tracking with geolocation
  - Request path and timestamp logging
  - Country and city resolution

- **🔒 Intelligent IP Security**
  - Automatic blocking of repeat offenders
  - Suspicious activity detection (100+ requests/hour)
  - Sensitive endpoint monitoring (`/login`, `/admin`)

- **⚡ Background Processing**
  - Hourly Celery tasks for IP analysis
  - Scalable task queue architecture
  - Automated threat detection

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | Django | Web framework & API |
| **Rate Limiting** | Django Ratelimit | Request throttling |
| **Task Queue** | Celery | Background job processing |
| **Cache & Broker** | Redis | Caching, rate limiting & task brokering |
| **Database** | SQLite/PostgreSQL | Data persistence |

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Redis server
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/loutimi/alx-backend-security.git
   cd alx-backend-security
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   
   # Linux/macOS
   source venv/bin/activate
   
   # Windows
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start Redis server**
   ```bash
   redis-server
   ```

5. **Configure Django settings**
   
   Add to your `settings.py`:
   ```python
   # Redis Cache Configuration
   CACHES = {
       "default": {
           "BACKEND": "django.core.cache.backends.redis.RedisCache",
           "LOCATION": "redis://127.0.0.1:6379/1",
       }
   }
   
   # Rate limiting
   RATELIMIT_USE_CACHE = "default"
   
   # Celery Configuration
   CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
   CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"
   ```

6. **Initialize database**
   ```bash
   python manage.py migrate
   ```

### Running the Application

Start all required services:

```bash
# Terminal 1: Django development server
python manage.py runserver

# Terminal 2: Celery worker
celery -A alx-backend-security worker -l info

# Terminal 3: Celery beat scheduler
celery -A alx-backend-security beat -l info
```

## 📂 Project Architecture

```
alx-backend-security/
├── ip_tracking/
│   ├── models.py          # Data models (RequestLog, BlockedIP, SuspiciousIP)
│   ├── tasks.py           # Celery background tasks
│   ├── views.py           # Rate-limited authentication views
│   ├── middleware.py      # Request logging with geolocation
│   └── urls.py            # URL routing
├── alx-backend-security/
│   ├── celery.py          # Celery configuration
│   ├── settings.py        # Django settings
│   └── urls.py            # Main URL configuration
├── requirements.txt       # Python dependencies
└── manage.py             # Django management script
```

## 🗄️ Database Models

### RequestLog
Tracks all incoming requests with comprehensive metadata.

| Field | Type | Description |
|-------|------|-------------|
| `ip_address` | GenericIPAddressField | Client IP address |
| `timestamp` | DateTimeField | Request timestamp (auto-generated) |
| `path` | CharField | Accessed endpoint |
| `country` | CharField (nullable) | Geolocation country |
| `city` | CharField (nullable) | Geolocation city |

### BlockedIP
Maintains permanently blocked IP addresses.

| Field | Type | Description |
|-------|------|-------------|
| `ip_address` | GenericIPAddressField | Blocked IP address |
| `reason` | TextField | Blocking reason |
| `blocked_at` | DateTimeField | When IP was blocked |

### SuspiciousIP
Records IPs flagged for suspicious activity.

| Field | Type | Description |
|-------|------|-------------|
| `ip_address` | GenericIPAddressField | Flagged IP address |
| `reason` | CharField | Flagging reason |
| `timestamp` | DateTimeField | When flagged |
| `request_count` | IntegerField | Number of requests in timeframe |

## ⚙️ Security Rules

### Rate Limiting
- **Anonymous users**: 5 requests per minute
- **Authenticated users**: 10 requests per minute
- **Rate limit key**: IP address for anonymous, User ID for authenticated

### Suspicious Activity Detection
- **High volume**: More than 100 requests per hour
- **Sensitive endpoints**: Repeated access to `/login`, `/admin`, `/api/auth/`
- **Automated blocking**: IPs exceeding thresholds are automatically flagged

### Background Monitoring
- **Hourly analysis**: Celery task reviews request patterns
- **Intelligent flagging**: Multi-criteria suspicious activity detection
- **Escalation**: Repeated offenders moved to permanent block list

## 🔧 Configuration Options

### Rate Limiting Settings
```python
RATELIMITS = {
    'anonymous': '5/m',      # 5 requests per minute
    'authenticated': '10/m', # 10 requests per minute
}
```

## 📈 Monitoring & Analytics

The system provides comprehensive monitoring through:

- **Real-time request logging**
- **Geographic IP tracking**
- **Suspicious activity alerts**
- **Automated threat response**
- **Historical data analysis**


## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Rotimi Musa**  
Backend Developer | Security Enthusiast  
🐙 [GitHub](https://github.com/loutimi)

---

<div align="center">
  <strong>Built with ❤️ for Django security</strong>
</div>