# Django URL Shortener with Analytics

A high-performance URL shortener built with Python, Django REST Framework, and Redis. It features built-in click analytics, per-key rate limiting, and an optimized hot-link caching mechanism designed to massively reduce database reads.

## Features

- **URL Shortening:** Generates a unique 6-character short code for any given long URL.
- **Click Analytics:** Asynchronously records the timestamp and IP address of every click, and tracks total click counts.
- **Hot-Link Caching:** Caches the destination URL and database ID directly into memory on the first click. Subsequent clicks are redirected instantly without performing a single synchronous database read.
- **Asynchronous Processing:** Analytics and click tracking are handled in a background thread to ensure the 302 redirect happens in milliseconds.
- **Rate Limiting:** Protects the API against spam with DRF rate limiting (configured for 10 requests/min for anonymous users, 100/min for logged-in users).
- **Simple UI:** Includes a clean web interface to easily submit and shorten URLs.

## Tech Stack

- **Backend:** Python 3, Django, Django REST Framework
- **Database:** SQLite (default) / PostgreSQL (recommended for production)
- **Caching:** Redis (via `django-redis`), temporarily using `LocMemCache` for easy local development.

## Getting Started

### Prerequisites
- Python 3.8+
- (Optional but recommended) Redis server running on port 6379.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/lakshyagupta127/URL-Shortener.git
   cd URL-Shortener
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install django djangorestframework redis django-redis
   ```

4. **Run Database Migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Start the Development Server:**
   ```bash
   python manage.py runserver
   ```

### Usage
- Open your browser and go to `http://127.0.0.1:8000/` to use the frontend UI.
- Alternatively, you can use the API directly:
  - **Create a short URL:** `POST /api/urls/` with body `{"original_url": "https://example.com"}`
  - **View Analytics:** `GET /api/analytics/<short_code>/`

## Performance Note
By default, the `settings.py` file is configured to use Django's `LocMemCache` for simple out-of-the-box local testing. For production, switch the `CACHES` configuration back to `django_redis.cache.RedisCache`.
