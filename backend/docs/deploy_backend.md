Excellent! I'm glad it's working. Here's a **unified, step-by-step guide** for deploying any Django backend to PythonAnywhere in the future.

---

# Complete Guide: Deploy Django Backend to PythonAnywhere

## 📋 Prerequisites

| Requirement | Details |
|-------------|---------|
| PythonAnywhere account | Free tier (Beginners account) |
| GitHub repository | Your Django project pushed to GitHub |
| Django project | Must have requirements.txt and proper structure |

---

## 🚀 Step-by-Step Deployment

### Step 1: Prepare Your Django Project for Production

Update your `settings.py` with these additions:

```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Add PythonAnywhere domain to allowed hosts
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.pythonanywhere.com']

# Static files configuration (MUST have these)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Media files (optional)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# CORS settings (for React frontend)
CORS_ALLOW_ALL_ORIGINS = True  # For demo only
CORS_ALLOW_CREDENTIALS = True
```

### Step 2: Push Code to GitHub

```bash
git add .
git commit -m "Prepare for PythonAnywhere deployment"
git push origin main
```

---

### Step 3: On PythonAnywhere - Open Bash Console

1. Log into [PythonAnywhere](https://www.pythonanywhere.com)
2. Go to **"Consoles"** tab
3. Click **"Bash"**

---

### Step 4: Clone Your Repository

```bash
cd ~
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

**Replace `YOUR_USERNAME` and `YOUR_REPO_NAME`** with your GitHub details.

---

### Step 5: Create Virtual Environment

```bash
# Create virtual environment (use Python 3.10 for best compatibility)
mkvirtualenv --python=/usr/bin/python3.10 myproject-env

# It auto-activates. If not:
workon myproject-env
```

**Naming tip:** Use a descriptive name like `myproject-env` or `backend-prod`

---

### Step 6: Install Dependencies

```bash
cd ~/YOUR_REPO_NAME/  # Navigate to where manage.py is
pip install -r requirements.txt
```

**If you don't have requirements.txt:**
```bash
pip install Django djangorestframework django-cors-headers gunicorn
```

---

### Step 7: Run Django Setup Commands

```bash
# Create database tables
python manage.py makemigrations
python manage.py migrate

# Collect static files (IMPORTANT!)
python manage.py collectstatic --noinput

# Create superuser (optional, for admin panel)
python manage.py createsuperuser
```

---

### Step 8: Configure the Web App

Go to **"Web"** tab → **"Add a new web app"**

Choose:
- **Manual configuration** (NOT the wizard)
- **Python 3.10** (or your version)

---

### Step 9: Configure Virtual Environment

In the **"Virtualenv"** section, enter:

```
/home/YOUR_USERNAME/.virtualenvs/myproject-env
```

**Replace `YOUR_USERNAME`** with your PythonAnywhere username.

---

### Step 10: Configure WSGI File

Under **"Code"** section, click the WSGI file link (e.g., `/var/www/YOUR_USERNAME_pythonanywhere_com_wsgi.py`)

**Replace everything with:**

```python
import os
import sys

# === CONFIGURATION - CHANGE THESE ===
username = 'YOUR_USERNAME'  # Your PythonAnywhere username
project_folder = 'YOUR_REPO_NAME'  # Your repository/folder name
python_version = '3.10'  # Your Python version (3.10, 3.11, etc.)
# === END CONFIGURATION ===

# Build paths
project_path = f'/home/{username}/{project_folder}'
venv_path = f'/home/{username}/.virtualenvs/myproject-env/lib/python{python_version}/site-packages'

# Add to system path
if project_path not in sys.path:
    sys.path.insert(0, project_path)
if venv_path not in sys.path:
    sys.path.insert(0, venv_path)

# Set Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'YOUR_PROJECT_NAME.settings'

# Setup Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Replace:**
- `YOUR_USERNAME` → your PythonAnywhere username
- `YOUR_REPO_NAME` → your repository name (where manage.py is)
- `myproject-env` → your virtual environment name
- `python_version` → your Python version
- `YOUR_PROJECT_NAME` → your Django project folder name (where settings.py is)

Click **"Save"**

---

### Step 11: Configure Static Files

Under **"Static files"** section, add:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/YOUR_USERNAME/YOUR_REPO_NAME/static` |

Click **"Add"**

---

### Step 12: Reload the Web App

Click the big green **"Reload"** button.

---

### Step 13: Test Your Deployment

Open your browser and go to:

```
https://YOUR_USERNAME.pythonanywhere.com/
```

Or test a specific endpoint:

```
https://YOUR_USERNAME.pythonanywhere.com/api/test/
```

---

## 🔧 Troubleshooting Common Issues

### Issue 1: "No module named 'django'"

**Fix:** Virtual environment path is wrong. In Bash console:
```bash
workon myproject-env
python -c "import site; print(site.getsitepackages())"
```
Use the output path in your WSGI file.

---

### Issue 2: "No module named 'your_project.settings'"

**Fix:** Check your project structure:
```bash
ls ~/YOUR_REPO_NAME/
# Should show manage.py
ls ~/YOUR_REPO_NAME/YOUR_PROJECT_NAME/
# Should show settings.py
```

---

### Issue 3: Static files not loading (404)

**Fix 1:** Run collectstatic again:
```bash
workon myproject-env
cd ~/YOUR_REPO_NAME/
python manage.py collectstatic --noinput
```

**Fix 2:** Verify static files directory:
```bash
ls ~/YOUR_REPO_NAME/static/
# Should show admin/, rest_framework/, etc.
```

---

### Issue 4: Database permission errors (SQLite)

**Fix:** Make the database writable:
```bash
cd ~/YOUR_REPO_NAME/
chmod 666 db.sqlite3
```

---

### Issue 5: 500 Internal Server Error

**Check error log:** Web tab → **"Error log"** link

Common causes:
- Missing environment variables
- Syntax error in WSGI file
- Wrong path in WSGI file

---

## 📝 Quick Reference Commands

| Action | Command |
|--------|---------|
| Open Bash console | Web tab → "Consoles" → "Bash" |
| Activate virtual env | `workon myproject-env` |
| Deactivate virtual env | `deactivate` |
| List virtual envs | `lsvirtualenv` |
| Delete virtual env | `rmvirtualenv myproject-env` |
| Update code from GitHub | `git pull origin main` |
| Run migrations | `python manage.py migrate` |
| Collect static files | `python manage.py collectstatic --noinput` |
| Reload web app | Click "Reload" button (can't do from CLI) |

---

## 🔄 Updating Your Deployed App

When you make changes to your code:

```bash
# 1. In Bash console
workon myproject-env
cd ~/YOUR_REPO_NAME/
git pull origin main

# 2. If dependencies changed
pip install -r requirements.txt

# 3. If database models changed
python manage.py migrate

# 4. If static files changed
python manage.py collectstatic --noinput

# 5. Go to Web tab → Click "Reload"
```

---

## 📊 Free Tier Limitations

| Limitation | Details |
|------------|---------|
| **Storage** | 512 MB |
| **CPU** | Shared, limited |
| **Sleep** | App sleeps after inactivity (wakes on request) |
| **Custom domain** | Not on free tier |
| **HTTPS** | Auto-provided for `*.pythonanywhere.com` |
| **Database** | SQLite only (no PostgreSQL on free tier) |
| **Requests** | Limited, but fine for demo |

---

## ✅ Deployment Checklist

| Step | Status |
|------|--------|
| 1. Django project with proper settings | ⬜ |
| 2. Code pushed to GitHub | ⬜ |
| 3. PythonAnywhere account created | ⬜ |
| 4. Repository cloned on PythonAnywhere | ⬜ |
| 5. Virtual environment created | ⬜ |
| 6. Requirements installed | ⬜ |
| 7. Migrations run | ⬜ |
| 8. Static files collected | ⬜ |
| 9. Web app created (Manual config) | ⬜ |
| 10. Virtualenv path set in Web tab | ⬜ |
| 11. WSGI file configured correctly | ⬜ |
| 12. Static files mapping added | ⬜ |
| 13. Web app reloaded | ⬜ |
| 14. Test URL works | ⬜ |

---

## 🎯 Key Takeaways

| Remember | Why |
|----------|-----|
| **Use Python 3.10** | Most compatible with Django |
| **Run collectstatic** | Required for static files to work |
| **Check error log first** | Always the first place to look for issues |
| **Reload after changes** | PythonAnywhere caches your code |
| **Set ALLOWED_HOSTS** | Include `.pythonanywhere.com` |
| **Use SQLite** | Free tier doesn't support PostgreSQL |

---

This guide should work for any Django project you deploy to PythonAnywhere in the future. Save it for reference!