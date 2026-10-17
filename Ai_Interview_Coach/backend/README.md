# AI Interview Coach Backend

A powerful, production-ready Flask backend for AI-powered interview preparation platform.

## 🚀 Features

- **Authentication & Authorization**: JWT-based secure authentication
- **Database Models**: Comprehensive data models for users, interviews, questions, answers, and feedback
- **AI-Powered Feedback**: Intelligent feedback generation for interview answers
- **Rate Limiting**: Protection against abuse with configurable rate limits
- **Caching**: Performance optimization with built-in caching
- **Analytics**: Detailed performance tracking and insights
- **RESTful API**: Well-structured API endpoints
- **Error Handling**: Comprehensive error handling and logging
- **Scalable Architecture**: Ready for production deployment

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd ai-interview-coach-backend
```

### 2. Create virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your configuration
# Change SECRET_KEY and JWT_SECRET_KEY to secure random strings
```

### 5. Initialize the database

```bash
python app.py
```

The application will automatically:
- Create the database
- Set up all tables
- Populate with 20+ sample questions

## 🏃‍♂️ Running the Application

### Development Mode

```bash
python app.py
```

The server will start on `http://localhost:5000`

### Production Mode

```bash
# Using Gunicorn (recommended for production)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# With more workers
gunicorn -w 8 --threads 4 -b 0.0.0.0:5000 app:app
```

## 📚 API Documentation

### Base URL
```
http://localhost:5000
```

### Authentication Endpoints

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword",
  "firstName": "John",
  "lastName": "Doe"
}

Response: 201 Created
{
  "message": "User registered successfully",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": { ... }
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}

Response: 200 OK
{
  "message": "Login successful",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": { ... }
}
```

#### Get Current User
```http
GET /api/auth/me
Authorization: Bearer <token>

Response: 200 OK
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "firstName": "John",
    "lastName": "Doe",
    "subscriptionTier": "free"
  }
}
```

### Interview Endpoints

#### Start Interview
```http
POST /api/interviews/start
Authorization: Bearer <token>
Content-Type: application/json

{
  "field": "software",
  "level": "intermediate",
  "type": "technical",
  "mode": "text",
  "questionsTotal": 5
}

Response: 201 Created
{
  "message": "Interview started successfully",
  "interview": { ... }
}
```

#### Get User Interviews
```http
GET /api/interviews?page=1&per_page=10&status=completed
Authorization: Bearer <token>

Response: 200 OK
{
  "interviews": [ ... ],
  "total": 50,
  "pages": 5,
  "currentPage": 1
}
```

#### Complete Interview
```http
POST /api/interviews/<interview_uuid>/complete
Authorization: Bearer <token>
Content-Type: application/json

{
  "duration": 1800,
  "score": 8.5,
  "questionsAnswered": 5
}

Response: 200 OK
{
  "message": "Interview completed successfully",
  "interview": { ... }
}
```

### Question Endpoints

#### Get Random Question
```http
POST /api/questions/random
Authorization: Bearer <token>
Content-Type: application/json

{
  "field": "software",
  "level": "intermediate",
  "type": "technical"
}

Response: 200 OK
{
  "question": {
    "id": "uuid",
    "text": "Explain closures in JavaScript...",
    "category": "technical",
    "difficulty": "medium",
    "hint": "Think about scope..."
  }
}
```

#### Get All Questions
```http
GET /api/questions?page=1&per_page=20&field=software&level=intermediate
Authorization: Optional

Response: 200 OK
{
  "questions": [ ... ],
  "total": 100,
  "pages": 5,
  "currentPage": 1
}
```

### Answer & Feedback Endpoints

#### Submit Answer
```http
POST /api/answers/submit
Authorization: Bearer <token>
Content-Type: application/json

{
  "interviewId": "uuid",
  "questionId": "uuid",
  "answer": "Your detailed answer here...",
  "timeSpent": 300
}

Response: 201 Created
{
  "message": "Answer submitted successfully",
  "answer": { ... },
  "feedback": {
    "score": 8.5,
    "strengths": [ ... ],
    "improvements": [ ... ],
    "detailedFeedback": "..."
  }
}
```

### Analytics Endpoints

#### Get Analytics Overview
```http
GET /api/analytics/overview
Authorization: Bearer <token>

Response: 200 OK
{
  "totalInterviews": 24,
  "averageScore": 8.5,
  "totalPracticeTime": 43200,
  "currentStreak": 7,
  "totalQuestions": 120,
  "recentInterviews": [ ... ]
}
```

#### Get Performance Data
```http
GET /api/analytics/performance
Authorization: Bearer <token>

Response: 200 OK
{
  "performanceData": [
    {
      "date": "2026-02-01",
      "score": 8.5,
      "type": "technical"
    },
    ...
  ]
}
```

### Legacy Endpoints (Backward Compatible)

#### Legacy Question Route
```http
POST /question
Content-Type: application/json

{
  "field": "software",
  "level": "intermediate"
}

Response: 200 OK
{
  "field": "software",
  "level": "intermediate",
  "question": "Explain OOP concepts..."
}
```

## 🗄️ Database Schema

### Users Table
- id (Primary Key)
- uuid (Unique Identifier)
- email (Unique, Indexed)
- password_hash
- first_name, last_name
- subscription_tier (free, pro, enterprise)
- created_at, last_login
- is_active

### Interviews Table
- id (Primary Key)
- uuid (Unique Identifier)
- user_id (Foreign Key)
- field, level, interview_type
- started_at, completed_at
- duration_seconds, status
- overall_score, questions_answered

### Questions Table
- id (Primary Key)
- uuid (Unique Identifier)
- text, category, field, level
- difficulty, company, tags
- hint, sample_answer
- usage_count, avg_score

### Answers Table
- id (Primary Key)
- uuid (Unique Identifier)
- interview_id, question_id (Foreign Keys)
- text, audio_url, video_url
- score, time_spent_seconds

### Feedback Table
- id (Primary Key)
- uuid (Unique Identifier)
- user_id, answer_id (Foreign Keys)
- score, strengths, improvements
- detailed_feedback, ai_model

## 🔒 Security Features

- Password hashing with bcrypt
- JWT token authentication
- Rate limiting on sensitive endpoints
- CORS protection
- Input validation
- SQL injection prevention (SQLAlchemy ORM)
- XSS protection
- CSRF protection ready

## 📊 Performance Optimization

- Database query optimization
- Response caching (5 minutes for static data)
- Connection pooling
- Efficient pagination
- Index on frequently queried columns

## 🧪 Testing

```bash
# Install testing dependencies
pip install pytest pytest-flask pytest-cov

# Run tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html
```

## 📝 Logging

Logs are stored in the `logs/` directory:
- Application logs: `logs/interview_coach.log`
- Rotating file handler (10MB per file, 10 backups)
- Includes timestamps, log levels, and file locations

## 🚀 Deployment

### Heroku

```bash
# Install Heroku CLI
# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
heroku run python app.py  # Initialize database
```

### AWS EC2

```bash
# SSH into your EC2 instance
# Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv nginx

# Clone and setup
git clone <repo>
cd ai-interview-coach-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure Nginx as reverse proxy
# Use systemd for process management
```

### Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 🔧 Configuration

### Environment Variables

See `.env.example` for all available configuration options.

### Database

Default: SQLite (development)
Production: PostgreSQL recommended

Change `DATABASE_URL` in `.env`:
```
DATABASE_URL=postgresql://user:password@localhost/dbname
```

## 📈 Monitoring

- Health check endpoint: `/health`
- Status endpoint: `/api/status`
- Logs in `logs/` directory
- Optional: Integrate Sentry for error tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

MIT License - feel free to use for personal or commercial projects

## 🆘 Support

For issues and questions:
- Check existing issues
- Create a new issue with detailed description
- Include error logs and steps to reproduce

## 🎯 Roadmap

- [ ] Real AI integration (OpenAI GPT-4, Claude)
- [ ] Voice recognition for verbal practice
- [ ] Video analysis for body language
- [ ] Company-specific interview prep
- [ ] Peer interview matching
- [ ] Interview scheduler
- [ ] Mobile app backend
- [ ] GraphQL API
- [ ] WebSocket for real-time features
- [ ] Advanced analytics dashboard

## ⚡ Performance Tips

1. Use PostgreSQL in production
2. Enable Redis caching
3. Use CDN for static assets
4. Implement database connection pooling
5. Use Gunicorn with multiple workers
6. Enable gzip compression
7. Implement request queuing for heavy operations

---

Built with ❤️ for aspiring interview champions!
