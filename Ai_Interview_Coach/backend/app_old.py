"""
AI Interview Coach - Professional Backend Application
A powerful, scalable backend for AI-powered interview preparation
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from functools import wraps
import os
import json
import random
import uuid
import logging
from logging.handlers import RotatingFileHandler

# =================================
# APPLICATION INITIALIZATION
# =================================

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///interview_coach.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300

# Initialize Extensions
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:*", "http://127.0.0.1:*", "https://*.vercel.app"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

db = SQLAlchemy(app)
jwt = JWTManager(app)
cache = Cache(app)
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per hour"],
    storage_uri="memory://"
)

# Setup Logging
if not os.path.exists('logs'):
    os.mkdir('logs')
    
file_handler = RotatingFileHandler('logs/interview_coach.log', maxBytes=10240000, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('AI Interview Coach Backend startup')

# =================================
# DATABASE MODELS
# =================================

class User(db.Model):
    """User model for authentication and profile"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    profile_picture = db.Column(db.String(256))
    subscription_tier = db.Column(db.String(20), default='free')  # free, pro, enterprise
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    interviews = db.relationship('Interview', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    feedback = db.relationship('Feedback', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set user password"""
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.uuid,
            'email': self.email,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'profilePicture': self.profile_picture,
            'subscriptionTier': self.subscription_tier,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'lastLogin': self.last_login.isoformat() if self.last_login else None
        }

class Interview(db.Model):
    """Interview session model"""
    __tablename__ = 'interviews'
    
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Interview Details
    field = db.Column(db.String(100))
    level = db.Column(db.String(50))
    interview_type = db.Column(db.String(50))  # technical, behavioral, system-design, hr
    company = db.Column(db.String(100))
    mode = db.Column(db.String(20))  # text, voice, video
    
    # Session Info
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    duration_seconds = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='in_progress')  # in_progress, completed, abandoned
    
    # Performance
    overall_score = db.Column(db.Float)
    questions_answered = db.Column(db.Integer, default=0)
    questions_total = db.Column(db.Integer, default=5)
    
    # Relationships
    answers = db.relationship('Answer', backref='interview', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert interview to dictionary"""
        return {
            'id': self.uuid,
            'field': self.field,
            'level': self.level,
            'type': self.interview_type,
            'company': self.company,
            'mode': self.mode,
            'startedAt': self.started_at.isoformat() if self.started_at else None,
            'completedAt': self.completed_at.isoformat() if self.completed_at else None,
            'duration': self.duration_seconds,
            'status': self.status,
            'score': self.overall_score,
            'questionsAnswered': self.questions_answered,
            'questionsTotal': self.questions_total
        }

class Question(db.Model):
    """Question bank model"""
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    
    # Question Content
    text = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))  # technical, behavioral, etc.
    field = db.Column(db.String(100))
    level = db.Column(db.String(50))
    difficulty = db.Column(db.String(20))  # easy, medium, hard
    
    # Metadata
    company = db.Column(db.String(100))
    tags = db.Column(db.Text)  # JSON array as string
    hint = db.Column(db.Text)
    sample_answer = db.Column(db.Text)
    evaluation_criteria = db.Column(db.Text)  # JSON as string
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    usage_count = db.Column(db.Integer, default=0)
    avg_score = db.Column(db.Float)
    
    def to_dict(self):
        """Convert question to dictionary"""
        return {
            'id': self.uuid,
            'text': self.text,
            'category': self.category,
            'field': self.field,
            'level': self.level,
            'difficulty': self.difficulty,
            'company': self.company,
            'tags': json.loads(self.tags) if self.tags else [],
            'hint': self.hint
        }

class Answer(db.Model):
    """User answer model"""
    __tablename__ = 'answers'
    
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    interview_id = db.Column(db.Integer, db.ForeignKey('interviews.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    
    # Answer Content
    text = db.Column(db.Text)
    audio_url = db.Column(db.String(256))
    video_url = db.Column(db.String(256))
    
    # Performance
    score = db.Column(db.Float)
    time_spent_seconds = db.Column(db.Integer)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    feedback_entries = db.relationship('Feedback', backref='answer', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert answer to dictionary"""
        return {
            'id': self.uuid,
            'text': self.text,
            'score': self.score,
            'timeSpent': self.time_spent_seconds,
            'submittedAt': self.submitted_at.isoformat() if self.submitted_at else None
        }

class Feedback(db.Model):
    """AI-generated feedback model"""
    __tablename__ = 'feedback'
    
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    answer_id = db.Column(db.Integer, db.ForeignKey('answers.id'), nullable=False)
    
    # Feedback Content
    score = db.Column(db.Float)
    strengths = db.Column(db.Text)  # JSON array as string
    improvements = db.Column(db.Text)  # JSON array as string
    detailed_feedback = db.Column(db.Text)
    
    # AI Metadata
    ai_model = db.Column(db.String(50))
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert feedback to dictionary"""
        return {
            'id': self.uuid,
            'score': self.score,
            'strengths': json.loads(self.strengths) if self.strengths else [],
            'improvements': json.loads(self.improvements) if self.improvements else [],
            'detailedFeedback': self.detailed_feedback,
            'generatedAt': self.generated_at.isoformat() if self.generated_at else None
        }

# =================================
# HELPER FUNCTIONS
# =================================

def init_db():
    """Initialize database with sample data"""
    with app.app_context():
        db.create_all()
        
        # Add sample questions if database is empty
        if Question.query.count() == 0:
            sample_questions = get_sample_questions()
            for q in sample_questions:
                question = Question(**q)
                db.session.add(question)
            db.session.commit()
            app.logger.info(f'Added {len(sample_questions)} sample questions to database')

def get_sample_questions():
    """Get comprehensive sample questions"""
    return [
        # Software Engineering - Technical
        {
            'text': 'Explain the difference between let, const, and var in JavaScript. When would you use each?',
            'category': 'technical',
            'field': 'software',
            'level': 'intermediate',
            'difficulty': 'medium',
            'tags': json.dumps(['javascript', 'fundamentals', 'es6']),
            'hint': 'Think about scope, hoisting, and reassignment capabilities',
            'evaluation_criteria': json.dumps(['scope understanding', 'hoisting knowledge', 'practical examples'])
        },
        {
            'text': 'What is a closure in JavaScript? Provide a practical use case.',
            'category': 'technical',
            'field': 'software',
            'level': 'intermediate',
            'difficulty': 'medium',
            'tags': json.dumps(['javascript', 'closures', 'advanced']),
            'hint': 'Consider data privacy and function factories'
        },
        {
            'text': 'Explain the SOLID principles in object-oriented programming.',
            'category': 'technical',
            'field': 'software',
            'level': 'senior',
            'difficulty': 'hard',
            'tags': json.dumps(['oop', 'design-patterns', 'solid']),
            'hint': 'Each letter stands for a different principle'
        },
        {
            'text': 'What is the difference between SQL and NoSQL databases? When would you choose one over the other?',
            'category': 'technical',
            'field': 'software',
            'level': 'intermediate',
            'difficulty': 'medium',
            'tags': json.dumps(['databases', 'sql', 'nosql']),
            'hint': 'Think about data structure, scalability, and ACID properties'
        },
        {
            'text': 'Explain how RESTful APIs work and what makes an API RESTful.',
            'category': 'technical',
            'field': 'software',
            'level': 'intermediate',
            'difficulty': 'medium',
            'tags': json.dumps(['api', 'rest', 'http']),
            'hint': 'Consider HTTP methods, statelessness, and resource naming'
        },
        
        # Data Science - Technical
        {
            'text': 'What is overfitting in machine learning and how can you prevent it?',
            'category': 'technical',
            'field': 'data-science',
            'level': 'intermediate',
            'difficulty': 'medium',
            'tags': json.dumps(['ml', 'overfitting', 'validation']),
            'hint': 'Think about model complexity and validation techniques'
        },
        {
            'text': 'Explain the bias-variance tradeoff in machine learning.',
            'category': 'technical',
            'field': 'data-science',
            'level': 'senior',
            'difficulty': 'hard',
            'tags': json.dumps(['ml', 'statistics', 'model-evaluation']),
            'hint': 'Consider underfitting vs overfitting'
        },
        {
            'text': 'What is the difference between supervised and unsupervised learning?',
            'category': 'technical',
            'field': 'data-science',
            'level': 'entry',
            'difficulty': 'easy',
            'tags': json.dumps(['ml', 'fundamentals']),
            'hint': 'Think about labeled vs unlabeled data'
        },
        {
            'text': 'Explain how a Random Forest algorithm works.',
            'category': 'technical',
            'field': 'data-science',
            'level': 'intermediate',
            'difficulty': 'medium',
            'tags': json.dumps(['ml', 'algorithms', 'ensemble']),
            'hint': 'Consider decision trees and ensemble methods'
        },
        
        # Behavioral Questions
        {
            'text': 'Tell me about a time when you had to work with a difficult team member. How did you handle it?',
            'category': 'behavioral',
            'field': 'general',
            'level': 'entry',
            'difficulty': 'medium',
            'tags': json.dumps(['teamwork', 'conflict-resolution']),
            'hint': 'Use the STAR method: Situation, Task, Action, Result'
        },
        {
            'text': 'Describe a project where you had to learn a new technology quickly. What was your approach?',
            'category': 'behavioral',
            'field': 'general',
            'level': 'intermediate',
            'difficulty': 'medium',
            'tags': json.dumps(['learning', 'adaptability']),
            'hint': 'Focus on your learning process and the outcome'
        },
        {
            'text': 'Give me an example of a time when you failed. What did you learn from it?',
            'category': 'behavioral',
            'field': 'general',
            'level': 'entry',
            'difficulty': 'medium',
            'tags': json.dumps(['failure', 'growth', 'self-awareness']),
            'hint': 'Show accountability and growth mindset'
        },
        {
            'text': 'Tell me about a time when you had to make a difficult decision with incomplete information.',
            'category': 'behavioral',
            'field': 'general',
            'level': 'senior',
            'difficulty': 'hard',
            'tags': json.dumps(['decision-making', 'leadership']),
            'hint': 'Explain your decision-making framework'
        },
        
        # System Design
        {
            'text': 'Design a URL shortening service like bit.ly. Consider scalability and high availability.',
            'category': 'system-design',
            'field': 'software',
            'level': 'senior',
            'difficulty': 'hard',
            'tags': json.dumps(['system-design', 'scalability', 'databases']),
            'hint': 'Think about URL generation, storage, redirection, and analytics'
        },
        {
            'text': 'Design a social media news feed system like Twitter or Facebook.',
            'category': 'system-design',
            'field': 'software',
            'level': 'senior',
            'difficulty': 'hard',
            'tags': json.dumps(['system-design', 'distributed-systems']),
            'hint': 'Consider fan-out strategies, caching, and real-time updates'
        },
        
        # HR Questions
        {
            'text': 'Why do you want to work for our company?',
            'category': 'hr',
            'field': 'general',
            'level': 'entry',
            'difficulty': 'easy',
            'tags': json.dumps(['motivation', 'company-fit']),
            'hint': 'Research the company and align with their values'
        },
        {
            'text': 'Where do you see yourself in 5 years?',
            'category': 'hr',
            'field': 'general',
            'level': 'entry',
            'difficulty': 'easy',
            'tags': json.dumps(['career-goals', 'ambition']),
            'hint': 'Show ambition while being realistic'
        },
        {
            'text': 'What is your greatest strength and weakness?',
            'category': 'hr',
            'field': 'general',
            'level': 'entry',
            'difficulty': 'easy',
            'tags': json.dumps(['self-awareness', 'personal-development']),
            'hint': 'Be honest and show how you\'re working on your weakness'
        },
        {
            'text': 'Why are you leaving your current job?',
            'category': 'hr',
            'field': 'general',
            'level': 'intermediate',
            'difficulty': 'medium',
            'tags': json.dumps(['career-transition', 'motivation']),
            'hint': 'Focus on what you\'re looking for, not what you\'re running from'
        },
        
        # Product Management
        {
            'text': 'How would you prioritize features for a product roadmap?',
            'category': 'product',
            'field': 'product',
            'level': 'intermediate',
            'difficulty': 'medium',
            'tags': json.dumps(['product-management', 'prioritization']),
            'hint': 'Consider frameworks like RICE or MoSCoW'
        },
        {
            'text': 'How would you measure the success of a new feature?',
            'category': 'product',
            'field': 'product',
            'level': 'intermediate',
            'difficulty': 'medium',
            'tags': json.dumps(['metrics', 'kpis', 'product-management']),
            'hint': 'Think about user engagement, business impact, and leading/lagging indicators'
        },
    ]

def generate_ai_feedback(answer_text, question_text, category='technical', interview_type='technical', level='intermediate', field='software'):
    """
    Generate AI feedback using GPT-4 Agent
    """
    from ai_agent import AIInterviewAgent
    
    try:
        # Create AI agent
        agent = AIInterviewAgent(
            interview_type=interview_type or category,
            level=level,
            field=field
        )
        
        # Analyze answer using GPT-4
        feedback = agent.analyze_answer(question_text, answer_text)
        
        return {
            'score': feedback['score'],
            'strengths': feedback['strengths'],
            'improvements': feedback['improvements'],
            'detailed_feedback': feedback['detailed_feedback'],
            'content_score': feedback.get('technical_accuracy', feedback['score']),
            'structure_score': feedback.get('communication_clarity', feedback['score']),
            'communication_score': feedback.get('communication_clarity', feedback['score']),
            'technical_accuracy_score': feedback.get('technical_accuracy', feedback['score']),
            'action_items': feedback.get('next_steps', []),
            'learning_resources': [],
            'practice_suggestions': feedback.get('missing_concepts', []),
            'ai_model': 'gpt-4',
            'ai_confidence_score': 0.95,
            'ai_processing_time': 0,
            'ai_tokens_used': feedback.get('answer_length', 0) * 2
        }
        
    except Exception as e:
        print(f"AI Agent error: {e}")
        # Fallback to simple scoring
        word_count = len(answer_text.split())
        base_score = min(10.0, max(4.0, word_count / 10))
        
        return {
            'score': base_score,
            'strengths': ['Provided a response'],
            'improvements': ['Add more detail'],
            'detailed_feedback': 'Good attempt. Add more specific examples.',
            'content_score': base_score,
            'structure_score': base_score,
            'communication_score': base_score,
            'technical_accuracy_score': base_score,
            'action_items': [],
            'learning_resources': [],
            'practice_suggestions': [],
            'ai_model': 'fallback',
            'ai_confidence_score': 0.5,
            'ai_processing_time': 0,
            'ai_tokens_used': 0
        }
# =================================
# AUTHENTICATION ROUTES
# =================================

@app.route('/api/auth/register', methods=['POST'])
@limiter.limit("5 per hour")
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validation
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Check if user exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 409
        
        # Create new user
        user = User(
            email=data['email'],
            first_name=data.get('firstName', ''),
            last_name=data.get('lastName', ''),
            subscription_tier='free'
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        # Create access token
        access_token = create_access_token(identity=user.uuid)
        
        app.logger.info(f'New user registered: {user.email}')
        
        return jsonify({
            'message': 'User registered successfully',
            'token': access_token,
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        app.logger.error(f'Registration error: {str(e)}')
        db.session.rollback()
        return jsonify({'error': 'Registration failed'}), 500

@app.route('/api/auth/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        # Validation
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Find user
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Account is deactivated'}), 403
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Create access token
        access_token = create_access_token(identity=user.uuid)
        
        app.logger.info(f'User logged in: {user.email}')
        
        return jsonify({
            'message': 'Login successful',
            'token': access_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        app.logger.error(f'Login error: {str(e)}')
        return jsonify({'error': 'Login failed'}), 500

@app.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user profile"""
    try:
        current_user_uuid = get_jwt_identity()
        user = User.query.filter_by(uuid=current_user_uuid).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        app.logger.error(f'Get user error: {str(e)}')
        return jsonify({'error': 'Failed to fetch user'}), 500

# =================================
# INTERVIEW ROUTES
# =================================

@app.route('/api/interviews/start', methods=['POST'])
@jwt_required()
@limiter.limit("20 per hour")
def start_interview():
    """Start a new interview session"""
    try:
        current_user_uuid = get_jwt_identity()
        user = User.query.filter_by(uuid=current_user_uuid).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Create new interview session
        interview = Interview(
            user_id=user.id,
            field=data.get('field'),
            level=data.get('level'),
            interview_type=data.get('type', 'technical'),
            company=data.get('company'),
            mode=data.get('mode', 'text'),
            questions_total=data.get('questionsTotal', 5),
            status='in_progress'
        )
        
        db.session.add(interview)
        db.session.commit()
        
        app.logger.info(f'Interview started: {interview.uuid} by user {user.email}')
        
        return jsonify({
            'message': 'Interview started successfully',
            'interview': interview.to_dict()
        }), 201
        
    except Exception as e:
        app.logger.error(f'Start interview error: {str(e)}')
        db.session.rollback()
        return jsonify({'error': 'Failed to start interview'}), 500

@app.route('/api/interviews/<interview_uuid>/complete', methods=['POST'])
@jwt_required()
def complete_interview(interview_uuid):
    """Complete an interview session"""
    try:
        current_user_uuid = get_jwt_identity()
        user = User.query.filter_by(uuid=current_user_uuid).first()
        
        interview = Interview.query.filter_by(uuid=interview_uuid, user_id=user.id).first()
        
        if not interview:
            return jsonify({'error': 'Interview not found'}), 404
        
        data = request.get_json()
        
        # Update interview
        interview.completed_at = datetime.utcnow()
        interview.duration_seconds = data.get('duration', 0)
        interview.overall_score = data.get('score', 0)
        interview.questions_answered = data.get('questionsAnswered', 0)
        interview.status = 'completed'
        
        db.session.commit()
        
        app.logger.info(f'Interview completed: {interview.uuid}')
        
        return jsonify({
            'message': 'Interview completed successfully',
            'interview': interview.to_dict()
        }), 200
        
    except Exception as e:
        app.logger.error(f'Complete interview error: {str(e)}')
        db.session.rollback()
        return jsonify({'error': 'Failed to complete interview'}), 500

@app.route('/api/interviews', methods=['GET'])
@jwt_required()
@cache.cached(timeout=60, query_string=True)
def get_user_interviews():
    """Get user's interview history"""
    try:
        current_user_uuid = get_jwt_identity()
        user = User.query.filter_by(uuid=current_user_uuid).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status')
        
        # Build query
        query = Interview.query.filter_by(user_id=user.id)
        
        if status:
            query = query.filter_by(status=status)
        
        # Paginate
        interviews = query.order_by(Interview.started_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'interviews': [i.to_dict() for i in interviews.items],
            'total': interviews.total,
            'pages': interviews.pages,
            'currentPage': page
        }), 200
        
    except Exception as e:
        app.logger.error(f'Get interviews error: {str(e)}')
        return jsonify({'error': 'Failed to fetch interviews'}), 500

# =================================
# QUESTION ROUTES
# =================================

@app.route('/api/questions/random', methods=['POST'])
@jwt_required()
@limiter.limit("50 per hour")
def get_random_question():
    """Get a random question based on criteria"""
    try:
        data = request.get_json()
        
        field = data.get('field')
        level = data.get('level')
        category = data.get('type', 'technical')
        
        # Build query
        query = Question.query
        
        if field:
            query = query.filter_by(field=field)
        if level:
            query = query.filter_by(level=level)
        if category:
            query = query.filter_by(category=category)
        
        # Get random question
        questions = query.all()
        
        if not questions:
            # Fallback to any question
            questions = Question.query.all()
        
        if not questions:
            return jsonify({'error': 'No questions available'}), 404
        
        question = random.choice(questions)
        
        # Increment usage count
        question.usage_count += 1
        db.session.commit()
        
        return jsonify({
            'question': question.to_dict()
        }), 200
        
    except Exception as e:
        app.logger.error(f'Get question error: {str(e)}')
        return jsonify({'error': 'Failed to fetch question'}), 500

@app.route('/api/questions', methods=['GET'])
@cache.cached(timeout=300, query_string=True)
def get_questions():
    """Get all questions with filters"""
    try:
        # Query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        field = request.args.get('field')
        level = request.args.get('level')
        category = request.args.get('category')
        difficulty = request.args.get('difficulty')
        
        # Build query
        query = Question.query
        
        if field:
            query = query.filter_by(field=field)
        if level:
            query = query.filter_by(level=level)
        if category:
            query = query.filter_by(category=category)
        if difficulty:
            query = query.filter_by(difficulty=difficulty)
        
        # Paginate
        questions = query.order_by(Question.usage_count.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'questions': [q.to_dict() for q in questions.items],
            'total': questions.total,
            'pages': questions.pages,
            'currentPage': page
        }), 200
        
    except Exception as e:
        app.logger.error(f'Get questions error: {str(e)}')
        return jsonify({'error': 'Failed to fetch questions'}), 500

@app.route('/api/questions/<question_uuid>', methods=['GET'])
@cache.cached(timeout=300)
def get_question(question_uuid):
    """Get a specific question"""
    try:
        question = Question.query.filter_by(uuid=question_uuid).first()
        
        if not question:
            return jsonify({'error': 'Question not found'}), 404
        
        return jsonify({'question': question.to_dict()}), 200
        
    except Exception as e:
        app.logger.error(f'Get question error: {str(e)}')
        return jsonify({'error': 'Failed to fetch question'}), 500

# =================================
# ANSWER & FEEDBACK ROUTES
# =================================

@app.route('/api/answers/submit', methods=['POST'])
@jwt_required()
@limiter.limit("30 per hour")
def submit_answer():
    """Submit an answer and get AI feedback"""
    try:
        current_user_uuid = get_jwt_identity()
        user = User.query.filter_by(uuid=current_user_uuid).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        interview_uuid = data.get('interviewId')
        question_uuid = data.get('questionId')
        answer_text = data.get('answer', '')
        time_spent = data.get('timeSpent', 0)
        
        # Validate interview
        interview = Interview.query.filter_by(uuid=interview_uuid, user_id=user.id).first()
        if not interview:
            return jsonify({'error': 'Interview not found'}), 404
        
        # Get question
        question = Question.query.filter_by(uuid=question_uuid).first()
        
        # --- CALLING THE UPDATED AI FEEDBACK FUNCTION ---
        # We extract metadata from the interview/question objects to feed the AI
        feedback_data = generate_ai_feedback(
            answer_text=answer_text, 
            question_text=question.text if question else 'General Interview Question', 
            category=question.category if question else 'technical',
            interview_type=getattr(interview, 'interview_type', 'technical'),
            level=getattr(interview, 'difficulty_level', 'intermediate'),
            field=getattr(interview, 'target_field', 'software')
        )
        # ------------------------------------------------
        
        # Create answer record
        answer = Answer(
            interview_id=interview.id,
            question_id=question.id if question else None,
            text=answer_text,
            time_spent_seconds=time_spent,
            score=feedback_data['score']
        )
        
        db.session.add(answer)
        db.session.flush()  # Get answer ID for the feedback record
        
        # Create feedback record using the enriched data from feedback_data
        feedback = Feedback(
            user_id=user.id,
            answer_id=answer.id,
            score=feedback_data['score'],
            strengths=json.dumps(feedback_data['strengths']),
            improvements=json.dumps(feedback_data['improvements']),
            detailed_feedback=feedback_data['detailed_feedback'],
            ai_model=feedback_data['ai_model'],
            # Optional: If your Feedback model has these columns, add them here:
            # content_score=feedback_data['content_score'],
            # technical_accuracy=feedback_data['technical_accuracy_score']
        )
        
        db.session.add(feedback)
        
        # Update interview stats
        interview.questions_answered += 1
        
        db.session.commit()
        
        app.logger.info(f'AI Feedback generated for {user.uuid} using {feedback_data["ai_model"]}')
        
        return jsonify({
            'message': 'Answer submitted successfully',
            'answer': answer.to_dict(),
            'feedback': feedback_data # Sending full feedback back to frontend
        }), 201
        
    except Exception as e:
        app.logger.error(f'Submit answer error: {str(e)}')
        db.session.rollback()
        return jsonify({'error': 'Failed to submit answer'}), 500
    
@app.route('/api/feedback/<answer_uuid>', methods=['GET'])
@jwt_required()
def get_feedback(answer_uuid):
    """Get feedback for a specific answer"""
    try:
        current_user_uuid = get_jwt_identity()
        user = User.query.filter_by(uuid=current_user_uuid).first()
        
        answer = Answer.query.filter_by(uuid=answer_uuid).first()
        
        if not answer:
            return jsonify({'error': 'Answer not found'}), 404
        
        feedback = Feedback.query.filter_by(answer_id=answer.id, user_id=user.id).first()
        
        if not feedback:
            return jsonify({'error': 'Feedback not found'}), 404
        
        return jsonify({'feedback': feedback.to_dict()}), 200
        
    except Exception as e:
        app.logger.error(f'Get feedback error: {str(e)}')
        return jsonify({'error': 'Failed to fetch feedback'}), 500

# =================================
# ANALYTICS ROUTES
# =================================

@app.route('/api/analytics/overview', methods=['GET'])
@jwt_required()
@cache.cached(timeout=120)
def get_analytics_overview():
    """Get user analytics overview"""
    try:
        current_user_uuid = get_jwt_identity()
        user = User.query.filter_by(uuid=current_user_uuid).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Calculate stats
        total_interviews = Interview.query.filter_by(user_id=user.id, status='completed').count()
        
        # Average score
        completed_interviews = Interview.query.filter_by(user_id=user.id, status='completed').all()
        avg_score = sum(i.overall_score or 0 for i in completed_interviews) / len(completed_interviews) if completed_interviews else 0
        
        # Total practice time
        total_time = sum(i.duration_seconds or 0 for i in completed_interviews)
        
        # Current streak (simplified)
        recent_interviews = Interview.query.filter_by(user_id=user.id, status='completed').order_by(Interview.completed_at.desc()).limit(7).all()
        streak = len(recent_interviews)
        
        # Performance by category
        answers = Answer.query.join(Interview).filter(Interview.user_id == user.id).all()
        total_questions = len(answers)
        
        return jsonify({
            'totalInterviews': total_interviews,
            'averageScore': round(avg_score, 1),
            'totalPracticeTime': total_time,
            'currentStreak': streak,
            'totalQuestions': total_questions,
            'recentInterviews': [i.to_dict() for i in recent_interviews[:5]]
        }), 200
        
    except Exception as e:
        app.logger.error(f'Get analytics error: {str(e)}')
        return jsonify({'error': 'Failed to fetch analytics'}), 500

@app.route('/api/analytics/performance', methods=['GET'])
@jwt_required()
@cache.cached(timeout=120)
def get_performance_data():
    """Get detailed performance data for charts"""
    try:
        current_user_uuid = get_jwt_identity()
        user = User.query.filter_by(uuid=current_user_uuid).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get last 30 days of interviews
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        interviews = Interview.query.filter(
            Interview.user_id == user.id,
            Interview.status == 'completed',
            Interview.completed_at >= thirty_days_ago
        ).order_by(Interview.completed_at).all()
        
        # Format for chart
        performance_data = [
            {
                'date': i.completed_at.strftime('%Y-%m-%d'),
                'score': i.overall_score,
                'type': i.interview_type
            }
            for i in interviews
        ]
        
        return jsonify({'performanceData': performance_data}), 200
        
    except Exception as e:
        app.logger.error(f'Get performance data error: {str(e)}')
        return jsonify({'error': 'Failed to fetch performance data'}), 500

# =================================
# ADMIN ROUTES
# =================================

@app.route('/api/admin/questions', methods=['POST'])
@jwt_required()
@limiter.limit("10 per hour")
def create_question():
    """Create a new question (admin only)"""
    try:
        # In production, add admin role check here
        data = request.get_json()
        
        question = Question(
            text=data.get('text'),
            category=data.get('category'),
            field=data.get('field'),
            level=data.get('level'),
            difficulty=data.get('difficulty', 'medium'),
            company=data.get('company'),
            tags=json.dumps(data.get('tags', [])),
            hint=data.get('hint'),
            sample_answer=data.get('sampleAnswer'),
            evaluation_criteria=json.dumps(data.get('evaluationCriteria', []))
        )
        
        db.session.add(question)
        db.session.commit()
        
        app.logger.info(f'Question created: {question.uuid}')
        
        return jsonify({
            'message': 'Question created successfully',
            'question': question.to_dict()
        }), 201
        
    except Exception as e:
        app.logger.error(f'Create question error: {str(e)}')
        db.session.rollback()
        return jsonify({'error': 'Failed to create question'}), 500

@app.route('/api/admin/stats', methods=['GET'])
@jwt_required()
@cache.cached(timeout=300)
def get_admin_stats():
    """Get platform statistics (admin only)"""
    try:
        # In production, add admin role check here
        total_users = User.query.count()
        total_interviews = Interview.query.count()
        total_questions = Question.query.count()
        active_users = User.query.filter_by(is_active=True).count()
        
        # Recent activity
        recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
        recent_interviews = Interview.query.order_by(Interview.started_at.desc()).limit(10).all()
        
        return jsonify({
            'totalUsers': total_users,
            'activeUsers': active_users,
            'totalInterviews': total_interviews,
            'totalQuestions': total_questions,
            'recentUsers': [u.to_dict() for u in recent_users],
            'recentInterviews': [i.to_dict() for i in recent_interviews]
        }), 200
        
    except Exception as e:
        app.logger.error(f'Get admin stats error: {str(e)}')
        return jsonify({'error': 'Failed to fetch statistics'}), 500

# =================================
# LEGACY ROUTES (for backward compatibility)
# =================================

@app.route('/question', methods=['GET', 'POST'])
def legacy_question_route():
    """Legacy question route for backward compatibility"""
    if request.method == 'GET':
        return jsonify({
            'message': 'Question endpoint is working. Use POST to send data.',
            'info': 'This is a legacy endpoint. Please use /api/questions/random instead.'
        })
    
    try:
        data = request.json
        field = data.get('field')
        level = data.get('level')
        
        # Try to get from database
        query = Question.query
        
        if field:
            query = query.filter_by(field=field)
        if level:
            query = query.filter_by(level=level)
        
        questions = query.all()
        
        if questions:
            question = random.choice(questions)
            return jsonify({
                'field': field,
                'level': level,
                'question': question.text,
                'category': question.category,
                'difficulty': question.difficulty
            })
        
        # Fallback to hardcoded questions
        fallback_questions = {
            'software': {
                'entry': 'What is a programming language?',
                'mid': 'Explain Object-Oriented Programming concepts.',
                'senior': 'Explain system design principles.'
            },
            'data-science': {
                'entry': 'What is data science?',
                'mid': 'What is overfitting in machine learning?',
                'senior': 'Explain the bias-variance tradeoff.'
            }
        }
        
        question_text = fallback_questions.get(field, {}).get(level, 'No question found')
        
        return jsonify({
            'field': field,
            'level': level,
            'question': question_text
        })
        
    except Exception as e:
        app.logger.error(f'Legacy question error: {str(e)}')
        return jsonify({'error': 'Failed to fetch question'}), 500

# =================================
# HEALTH CHECK & STATUS ROUTES
# =================================

@app.route('/', methods=['GET'])
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'AI Interview Coach Backend is running!',
        'version': '2.0.0',
        'timestamp': datetime.utcnow().isoformat(),
        'endpoints': {
            'auth': '/api/auth/*',
            'interviews': '/api/interviews/*',
            'questions': '/api/questions/*',
            'analytics': '/api/analytics/*',
            'admin': '/api/admin/*'
        }
    }), 200

@app.route('/api/status', methods=['GET'])
def api_status():
    """Detailed API status"""
    try:
        # Check database connection
        db.session.execute('SELECT 1')
        db_status = 'connected'
    except Exception:
        db_status = 'error'
    
    return jsonify({
        'api': 'operational',
        'database': db_status,
        'version': '2.0.0',
        'uptime': 'N/A',  # Implement actual uptime tracking if needed
        'totalUsers': User.query.count(),
        'totalInterviews': Interview.query.count(),
        'totalQuestions': Question.query.count()
    }), 200

# =================================
# ERROR HANDLERS
# =================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Resource not found',
        'message': str(error)
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    app.logger.error(f'Internal error: {str(error)}')
    db.session.rollback()
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500

@app.errorhandler(429)
def rate_limit_exceeded(error):
    """Handle rate limit errors"""
    return jsonify({
        'error': 'Rate limit exceeded',
        'message': 'Too many requests. Please try again later.'
    }), 429

@jwt.unauthorized_loader
def unauthorized_callback(callback):
    """Handle unauthorized access"""
    return jsonify({
        'error': 'Unauthorized',
        'message': 'Authentication required'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(callback):
    """Handle invalid token"""
    return jsonify({
        'error': 'Invalid token',
        'message': 'The provided token is invalid'
    }), 401

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    """Handle expired token"""
    return jsonify({
        'error': 'Token expired',
        'message': 'The provided token has expired'
    }), 401

# =================================
# APPLICATION STARTUP
# =================================

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Run application
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    app.logger.info(f'Starting AI Interview Coach Backend on port {port}')
    app.logger.info(f'Debug mode: {debug}')
    
    app.run(host='0.0.0.0', port=port, debug=debug)
