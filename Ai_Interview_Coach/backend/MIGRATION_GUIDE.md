# 🚀 ENTERPRISE DATABASE - COMPLETE SETUP & MIGRATION GUIDE

## 📋 TABLE OF CONTENTS
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Database Migration](#database-migration)
4. [Configuration](#configuration)
5. [Testing](#testing)
6. [Deployment](#deployment)
7. [Troubleshooting](#troubleshooting)

---

## ✅ PREREQUISITES

### Required Software
- **Python 3.9+** (3.10 or 3.11 recommended)
- **pip 23.0+**
- **SQLite 3.35+** OR **PostgreSQL 13+** OR **MySQL 8.0+**
- **Git 2.30+**

### Optional (for production)
- **Redis 7.0+** (for caching and real-time features)
- **Nginx 1.24+** (reverse proxy)
- **Docker 24.0+** (containerization)

---

## 📦 INSTALLATION

### Step 1: Backup Your Current Database

```bash
# Navigate to your backend folder
cd D:\ASIET\Projects\ai_coach_demo\backend

# Backup current database
copy interview_coach.db interview_coach_backup_$(date +%Y%m%d).db

# Export to SQL (optional)
sqlite3 interview_coach.db .dump > backup_$(date +%Y%m%d).sql
```

### Step 2: Install Enhanced Requirements

```bash
# Activate virtual environment (if not already)
venv\Scripts\activate  # Windows
# OR
source venv/bin/activate  # Linux/Mac

# Upgrade pip
python -m pip install --upgrade pip

# Install minimal core dependencies first
pip install Flask==3.0.0
pip install Flask-SQLAlchemy==3.1.1
pip install Flask-Migrate==4.0.5
pip install Flask-CORS==4.0.0
pip install Flask-JWT-Extended==4.6.0
pip install bcrypt==4.1.2
pip install python-dotenv==1.0.0

# Install all dependencies (this will take 10-15 minutes)
pip install -r requirements_enterprise.txt --no-cache-dir

# Verify installation
pip list | grep Flask
```

### Step 3: Replace Backend File

```bash
# Backup your current app.py
copy app.py app_old.py

# Copy the enhanced version
copy app_enhanced.py app.py

# Verify the file
python -c "import app; print('✅ App loaded successfully')"
```

---

## 🔄 DATABASE MIGRATION

### Option A: Fresh Install (Recommended for Testing)

```bash
# Remove old database
del interview_coach.db

# Initialize new enterprise database
python
>>> from app import init_db
>>> init_db()
>>> exit()

# Verify tables created
python
>>> from app import db
>>> from app import User, Interview, Question, Answer, Feedback
>>> print(f"Tables: {db.metadata.tables.keys()}")
>>> exit()
```

### Option B: Migration from Old Database

```bash
# Initialize Flask-Migrate
flask db init

# Create migration
flask db migrate -m "Upgrade to Enterprise Database v2.0"

# Review migration file (important!)
# Check: backend/migrations/versions/*.py

# Apply migration
flask db upgrade

# Verify migration
python
>>> from app import db
>>> db.engine.table_names()
>>> exit()
```

### Option C: Data Migration Script

Create `migrate_data.py`:

```python
"""
Data Migration Script
Migrates data from old database to enterprise database
"""

from datetime import datetime
import sqlite3
import sys

def migrate_users(old_conn, new_conn):
    """Migrate users table"""
    old_cursor = old_conn.cursor()
    new_cursor = new_conn.cursor()
    
    # Fetch old users
    old_cursor.execute("SELECT * FROM users")
    users = old_cursor.fetchall()
    
    print(f"Migrating {len(users)} users...")
    
    for user in users:
        # Map old fields to new fields
        new_cursor.execute("""
            INSERT INTO users (
                email, password_hash, first_name, last_name,
                subscription_tier, created_at, last_login,
                total_interviews, average_score
            ) VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0.0)
        """, (
            user[1],  # email
            user[2],  # password_hash
            user[3],  # first_name
            user[4],  # last_name
            user[5] or 'free',  # subscription_tier
            user[6],  # created_at
            user[7]   # last_login
        ))
    
    new_conn.commit()
    print("✅ Users migrated successfully")


def migrate_interviews(old_conn, new_conn):
    """Migrate interviews table"""
    old_cursor = old_conn.cursor()
    new_cursor = new_conn.cursor()
    
    # Get user ID mapping
    old_cursor.execute("SELECT id, uuid FROM users")
    user_map = {old_id: uuid for old_id, uuid in old_cursor.fetchall()}
    
    # Fetch old interviews
    old_cursor.execute("SELECT * FROM interviews")
    interviews = old_cursor.fetchall()
    
    print(f"Migrating {len(interviews)} interviews...")
    
    for interview in interviews:
        # Map fields
        new_cursor.execute("""
            INSERT INTO interviews (
                user_id, field, level, interview_type, company,
                mode, started_at, completed_at, duration_seconds,
                status, overall_score, questions_answered, questions_total
            ) VALUES (
                (SELECT id FROM users WHERE uuid = ?),
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
        """, (
            user_map.get(interview[1]),  # user_id
            interview[2],  # field
            interview[3],  # level
            interview[4],  # interview_type
            interview[5],  # company
            interview[6],  # mode
            interview[7],  # started_at
            interview[8],  # completed_at
            interview[9],  # duration_seconds
            interview[10], # status
            interview[11], # overall_score
            interview[12], # questions_answered
            interview[13]  # questions_total
        ))
    
    new_conn.commit()
    print("✅ Interviews migrated successfully")


def migrate_all():
    """Main migration function"""
    try:
        # Connect to databases
        old_db = sqlite3.connect('interview_coach.db')
        new_db = sqlite3.connect('interview_coach_enterprise.db')
        
        print("🚀 Starting data migration...")
        print("=" * 50)
        
        # Migrate tables
        migrate_users(old_db, new_db)
        migrate_interviews(old_db, new_db)
        
        # Update statistics
        print("\nUpdating user statistics...")
        new_cursor = new_db.cursor()
        new_cursor.execute("""
            UPDATE users SET
                total_interviews = (
                    SELECT COUNT(*) FROM interviews 
                    WHERE interviews.user_id = users.id
                ),
                average_score = (
                    SELECT AVG(overall_score) FROM interviews
                    WHERE interviews.user_id = users.id
                      AND status = 'completed'
                )
        """)
        new_db.commit()
        
        print("=" * 50)
        print("✅ Migration completed successfully!")
        print(f"\nMigrated:")
        print(f"  - Users: {len(users)}")
        print(f"  - Interviews: {len(interviews)}")
        
        # Close connections
        old_db.close()
        new_db.close()
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    migrate_all()
```

Run migration:
```bash
python migrate_data.py
```

---

## ⚙️ CONFIGURATION

### 1. Update Environment Variables

Edit `.env`:

```bash
# Application
FLASK_APP=app.py
FLASK_ENV=development  # Change to 'production' for production
SECRET_KEY=your-super-secret-key-here-change-this-in-production
JWT_SECRET_KEY=jwt-super-secret-key-here-change-this-too

# Database
DATABASE_URL=sqlite:///interview_coach_enterprise.db
# OR for PostgreSQL:
# DATABASE_URL=postgresql://username:password@localhost/interview_coach

# OR for MySQL:
# DATABASE_URL=mysql+pymysql://username:password@localhost/interview_coach

# Redis (for caching and real-time features)
REDIS_URL=redis://localhost:6379/0

# AI Models (optional)
OPENAI_API_KEY=your-openai-key-here
ANTHROPIC_API_KEY=your-anthropic-key-here
COHERE_API_KEY=your-cohere-key-here

# Email (for notifications)
SENDGRID_API_KEY=your-sendgrid-key-here
MAIL_FROM_EMAIL=noreply@aiinterviewcoach.com

# Monitoring (optional)
SENTRY_DSN=your-sentry-dsn-here

# Feature Flags
ENABLE_REAL_TIME_ANALYTICS=true
ENABLE_LEADERBOARDS=true
ENABLE_ACHIEVEMENTS=true
ENABLE_AI_FEEDBACK=true

# Performance
MAX_CONTENT_LENGTH=16777216  # 16MB
SQLALCHEMY_POOL_SIZE=10
SQLALCHEMY_MAX_OVERFLOW=20

# Security
SESSION_COOKIE_SECURE=true  # Only in production
SESSION_COOKIE_HTTPONLY=true
SESSION_COOKIE_SAMESITE=Lax
PERMANENT_SESSION_LIFETIME=604800  # 7 days
```

### 2. Initialize Database

```bash
python
>>> from app import db, init_db
>>> init_db()
>>> 
>>> # Verify tables
>>> print(db.metadata.tables.keys())
>>> 
>>> # Check sample questions
>>> from app import Question
>>> print(f"Sample questions: {Question.query.count()}")
>>> exit()
```

---

## 🧪 TESTING

### 1. Run Unit Tests

```bash
# Install test dependencies
pip install pytest pytest-flask pytest-cov

# Run tests
pytest tests/ -v --cov=app

# Generate coverage report
pytest --cov=app --cov-report=html
```

### 2. Test API Endpoints

```bash
# Start the server
python app.py

# In another terminal, test endpoints:

# Health check
curl http://localhost:5000/health

# Register user
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!",
    "firstName": "Test",
    "lastName": "User"
  }'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!"
  }'
```

### 3. Performance Testing

```bash
# Install locust
pip install locust

# Create locustfile.py
cat > locustfile.py << 'EOF'
from locust import HttpUser, task, between

class InterviewUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(1)
    def health_check(self):
        self.client.get("/health")
    
    @task(3)
    def get_questions(self):
        self.client.get("/api/questions")
EOF

# Run load test
locust -f locustfile.py --host=http://localhost:5000
```

---

## 🚀 DEPLOYMENT

### Option A: Traditional Server (Ubuntu/Debian)

```bash
# Install system dependencies
sudo apt update
sudo apt install python3-pip python3-venv nginx postgresql redis

# Setup PostgreSQL
sudo -u postgres createdb interview_coach
sudo -u postgres psql
postgres=# CREATE USER interview_user WITH PASSWORD 'secure_password';
postgres=# GRANT ALL PRIVILEGES ON DATABASE interview_coach TO interview_user;
postgres=# \q

# Clone repository
cd /var/www
git clone https://github.com/yourrepo/ai-interview-coach.git
cd ai-interview-coach/backend

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements_enterprise.txt

# Configure environment
cp .env.example .env
nano .env  # Edit configuration

# Initialize database
flask db upgrade

# Setup Gunicorn
pip install gunicorn

# Create systemd service
sudo nano /etc/systemd/system/interview-coach.service
```

Service file content:
```ini
[Unit]
Description=AI Interview Coach Backend
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/ai-interview-coach/backend
Environment="PATH=/var/www/ai-interview-coach/backend/venv/bin"
ExecStart=/var/www/ai-interview-coach/backend/venv/bin/gunicorn \
    --workers 4 \
    --bind 127.0.0.1:5000 \
    --timeout 120 \
    --access-logfile /var/log/interview-coach/access.log \
    --error-logfile /var/log/interview-coach/error.log \
    app:app

[Install]
WantedBy=multi-user.target
```

```bash
# Start service
sudo systemctl daemon-reload
sudo systemctl start interview-coach
sudo systemctl enable interview-coach

# Configure Nginx
sudo nano /etc/nginx/sites-available/interview-coach
```

Nginx configuration:
```nginx
server {
    listen 80;
    server_name api.yourdomain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/interview-coach /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Setup SSL (Let's Encrypt)
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d api.yourdomain.com
```

### Option B: Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements_enterprise.txt .
RUN pip install --no-cache-dir -r requirements_enterprise.txt

# Copy application
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 5000

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/interview_coach
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - ./logs:/app/logs
  
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=interview_coach
      - POSTGRES_PASSWORD=password
    volumes:
      - pgdata:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    volumes:
      - redisdata:/data

volumes:
  pgdata:
  redisdata:
```

Deploy:
```bash
docker-compose up -d
docker-compose logs -f backend
```

---

## 🔧 TROUBLESHOOTING

### Issue 1: Migration Fails

```bash
# Reset migrations
rm -rf migrations/
flask db init
flask db migrate
flask db upgrade

# Or manually create tables
python
>>> from app import db
>>> db.create_all()
```

### Issue 2: Import Errors

```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements_enterprise.txt

# Check Python path
python
>>> import sys
>>> print(sys.path)
```

### Issue 3: Database Connection Errors

```bash
# Check database file permissions
ls -la interview_coach_enterprise.db

# For PostgreSQL
psql -h localhost -U interview_user -d interview_coach

# For MySQL
mysql -h localhost -u interview_user -p interview_coach
```

### Issue 4: Performance Issues

```bash
# Check database indexes
python
>>> from app import db
>>> from sqlalchemy import inspect
>>> inspector = inspect(db.engine)
>>> for table in inspector.get_table_names():
>>>     print(f"\n{table}:")
>>>     for index in inspector.get_indexes(table):
>>>         print(f"  - {index['name']}")

# Vacuum database (SQLite)
sqlite3 interview_coach_enterprise.db "VACUUM;"

# Analyze database
sqlite3 interview_coach_enterprise.db "ANALYZE;"
```

### Issue 5: Memory Leaks

```bash
# Monitor memory usage
pip install memory_profiler

# Profile application
python -m memory_profiler app.py
```

---

## 📊 VERIFICATION CHECKLIST

After migration, verify:

- [ ] All tables created (13 tables total)
- [ ] Sample questions loaded (20+ questions)
- [ ] Indexes created properly
- [ ] User registration works
- [ ] Login works
- [ ] Interview creation works
- [ ] Answer submission works
- [ ] AI feedback generation works
- [ ] Analytics endpoints work
- [ ] Real-time features work
- [ ] Leaderboard updates
- [ ] Achievements tracked
- [ ] Activity logs recorded
- [ ] Database backups configured
- [ ] Monitoring enabled

---

## 🎯 POST-DEPLOYMENT

### 1. Database Backup Script

Create `backup.sh`:
```bash
#!/bin/bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/interview-coach"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
pg_dump interview_coach > $BACKUP_DIR/db_$TIMESTAMP.sql

# Compress
gzip $BACKUP_DIR/db_$TIMESTAMP.sql

# Delete old backups (keep last 30 days)
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete

echo "✅ Backup completed: db_$TIMESTAMP.sql.gz"
```

Schedule with cron:
```bash
crontab -e
# Add: 0 2 * * * /path/to/backup.sh
```

### 2. Monitoring

```bash
# Install monitoring tools
pip install flask-monitor datadog ddtrace

# Setup health check endpoint monitoring
# Use: Uptime Robot, Pingdom, or custom script
```

### 3. Logging

```bash
# Setup log rotation
sudo nano /etc/logrotate.d/interview-coach

# Add:
/var/log/interview-coach/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
}
```

---

## 📚 ADDITIONAL RESOURCES

- **Flask Documentation:** https://flask.palletsprojects.com/
- **SQLAlchemy Documentation:** https://docs.sqlalchemy.org/
- **PostgreSQL Documentation:** https://www.postgresql.org/docs/
- **Redis Documentation:** https://redis.io/documentation

---

**Migration Guide Version:** 2.0  
**Last Updated:** February 7, 2026  
**Support:** support@aiinterviewcoach.com
