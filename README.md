# lead_engine

Django 5.x backend with MySQL, Redis, and Celery.

## Tech Stack

- Python 3.11
- Django 5.2
- MySQL 9.x (port 3307)
- Redis 8.x (port 6379)
- Celery 5.x + django-celery-beat + django-celery-results
- Django REST Framework

## Prerequisites

Make sure the following are installed and running:

```bash
brew services start mysql   # port 3307
brew services start redis   # port 6379
```

## Local Setup

**1. Clone the repo**
```bash
git clone <repo-url>
cd lead_engine
```

**2. Create virtual environment**
```bash
python3.11 -m venv env
source env/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements/base.txt
```

**4. Configure environment**
```bash
cp lead_engine/settings/local_example.py lead_engine/settings/local.py
```

Create a `.env` file at the project root:
```bash
cp .env.example .env
```

Fill in your values:
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=lead_engine
DB_USER=root
DB_PASSWORD=
DB_HOST=127.0.0.1
DB_PORT=3307

REDIS_URL=redis://127.0.0.1:6379/0
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=django-db
```

**5. Create the database**
```bash
mysql -u root -P 3307 -e "CREATE DATABASE IF NOT EXISTS lead_engine CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

**6. Run migrations**
```bash
python manage.py migrate
```

**7. Start the development server**
```bash
python manage.py runserver
```

## Running Celery

**Worker** (processes tasks):
```bash
celery -A lead_engine worker --loglevel=info
```

**Beat** (schedules periodic tasks):
```bash
celery -A lead_engine beat --loglevel=info
```

## Settings

| File | Purpose |
|---|---|
| `lead_engine/settings/base.py` | Common config for all environments |
| `lead_engine/settings/local.py` | Local dev overrides — gitignored, create from `base.py` |
| `lead_engine/settings/production.py` | Production overrides — set via `DJANGO_SETTINGS_MODULE` env var |

## Environment Variable

Override settings module per environment:
```bash
# production
export DJANGO_SETTINGS_MODULE=lead_engine.settings.production
```

## Requirements

| File | Purpose |
|---|---|
| `requirements/base.txt` | Core dependencies |
| `requirements/dev.txt` | Dev dependencies (includes base) |
| `requirements/freeze.txt` | Fully pinned snapshot for reproducible deploys |
