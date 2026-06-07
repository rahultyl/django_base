# lead_engine

Django 5.x backend with MySQL, Redis, and Celery.

## Tech Stack

- Python 3.11
- Django 5.2
- MySQL 9.x (port 3307)
- Redis 8.x (port 6379)
- Celery 5.x
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
pip install -r requirements/dev.txt
```

**4. Install pre-commit hooks**
```bash
pre-commit install
```

> On macOS you may need to set SSL certs for pre-commit to work:
> ```bash
> export SSL_CERT_FILE=$(python3.11 -c "import certifi; print(certifi.where())")
> export REQUESTS_CA_BUNDLE=$SSL_CERT_FILE
> ```
> Add these to your `~/.zshrc` to make them permanent.

**5. Configure environment**

Create a `local.py` settings file:
```bash
cp lead_engine/settings/base.py lead_engine/settings/local.py
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
```

**6. Create the database**
```bash
mysql -u root -P 3307 -e "CREATE DATABASE IF NOT EXISTS lead_engine CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

**7. Run migrations**
```bash
python manage.py migrate
```

**8. Start the development server**
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

## Code Quality

This project uses [pre-commit](https://pre-commit.com/) hooks that run automatically on every commit:

| Hook | Purpose |
|---|---|
| `ruff` | Lint and auto-fix Python code |
| `ruff-format` | Format Python code |
| `gitleaks` | Detect hardcoded secrets |
| `trailing-whitespace` | Remove trailing whitespace |
| `check-added-large-files` | Block files over 500KB |

Run hooks manually across all files:
```bash
pre-commit run --all-files
```

## CI (GitHub Actions)

On every push and pull request to `main`:

| Workflow | Job | What it does |
|---|---|---|
| `Ruff` | `ruff` | Lint and format check |
| `Gitleaks` | `gitleaks` | Secret scanning |

## Settings

| File | Purpose |
|---|---|
| `lead_engine/settings/base.py` | Common config for all environments |
| `lead_engine/settings/local.py` | Local dev overrides — gitignored, create from `base.py` |
| `lead_engine/settings/production.py` | Production overrides — set via `DJANGO_SETTINGS_MODULE` env var |

Override settings module per environment:
```bash
export DJANGO_SETTINGS_MODULE=lead_engine.settings.production
```

## Requirements

| File | Purpose |
|---|---|
| `requirements/base.txt` | Core dependencies |
| `requirements/dev.txt` | Dev dependencies — includes base + pre-commit + ruff |
| `requirements/freeze.txt` | Fully pinned snapshot for reproducible deploys |
