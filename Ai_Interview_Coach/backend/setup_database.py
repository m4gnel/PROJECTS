#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Database Setup for AI Interview Coach"""

import sqlite3
import os
import uuid

DB_PATH = 'interview_coach.db'

def create_database():
    """Create database with all tables"""
    print("🔨 Creating AI Interview Coach Database...")
    
    # Delete old database if exists
    if os.path.exists(DB_PATH):
        print(f"⚠️  Found existing database")
        response = input("Delete and recreate? (y/n): ")
        if response.lower() != 'y':
            print("❌ Keeping existing database")
            return
        os.remove(DB_PATH)
        print("✅ Deleted old database")
    
    # Create connection
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("📊 Creating tables...")
    
    # Users table
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            first_name TEXT,
            last_name TEXT,
            profile_picture TEXT,
            subscription_tier TEXT DEFAULT 'free',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            is_active INTEGER DEFAULT 1,
            total_interviews INTEGER DEFAULT 0,
            total_practice_time INTEGER DEFAULT 0,
            average_score REAL DEFAULT 0.0,
            current_streak INTEGER DEFAULT 0,
            longest_streak INTEGER DEFAULT 0
        )
    ''')
    
    # Interviews table
    cursor.execute('''
        CREATE TABLE interviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE NOT NULL,
            user_id INTEGER NOT NULL,
            field TEXT,
            level TEXT,
            interview_type TEXT,
            company TEXT,
            mode TEXT DEFAULT 'text',
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            duration_seconds INTEGER DEFAULT 0,
            status TEXT DEFAULT 'in_progress',
            overall_score REAL,
            technical_score REAL,
            communication_score REAL,
            questions_answered INTEGER DEFAULT 0,
            questions_total INTEGER DEFAULT 5,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Questions table
    cursor.execute('''
        CREATE TABLE questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE NOT NULL,
            text TEXT NOT NULL,
            category TEXT,
            field TEXT,
            level TEXT,
            difficulty TEXT,
            company TEXT,
            tags TEXT,
            hint TEXT,
            sample_answer TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            usage_count INTEGER DEFAULT 0,
            avg_score REAL
        )
    ''')
    
    # Answers table
    cursor.execute('''
        CREATE TABLE answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE NOT NULL,
            interview_id INTEGER NOT NULL,
            question_id INTEGER,
            text TEXT,
            audio_url TEXT,
            video_url TEXT,
            score REAL,
            time_spent_seconds INTEGER,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (interview_id) REFERENCES interviews (id),
            FOREIGN KEY (question_id) REFERENCES questions (id)
        )
    ''')
    
    # Feedback table
    cursor.execute('''
        CREATE TABLE feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE NOT NULL,
            user_id INTEGER NOT NULL,
            answer_id INTEGER NOT NULL,
            score REAL,
            strengths TEXT,
            improvements TEXT,
            detailed_feedback TEXT,
            ai_model TEXT,
            generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (answer_id) REFERENCES answers (id)
        )
    ''')
    
    print("✅ Tables created successfully!")
    print("📝 Adding sample questions...")
    
    # Sample questions
    questions = [
        {
            'text': 'Explain the difference between let, const, and var in JavaScript. When would you use each?',
            'category': 'technical',
            'field': 'software',
            'level': 'intermediate',
            'difficulty': 'medium',
            'hint': 'Think about scope, hoisting, and reassignment'
        },
        {
            'text': 'What is the difference between SQL and NoSQL databases? When would you choose one over the other?',
            'category': 'technical',
            'field': 'software',
            'level': 'intermediate',
            'difficulty': 'medium',
            'hint': 'Consider data structure, scalability, and ACID properties'
        },
        {
            'text': 'Explain how RESTful APIs work and what makes an API RESTful.',
            'category': 'technical',
            'field': 'software',
            'level': 'intermediate',
            'difficulty': 'medium',
            'hint': 'Think about HTTP methods, statelessness, and resource naming'
        },
        {
            'text': 'What is a closure in JavaScript? Provide a practical use case.',
            'category': 'technical',
            'field': 'software',
            'level': 'intermediate',
            'difficulty': 'medium',
            'hint': 'Consider data privacy and function factories'
        },
        {
            'text': 'Tell me about a time when you had to work with a difficult team member. How did you handle it?',
            'category': 'behavioral',
            'field': 'general',
            'level': 'intermediate',
            'difficulty': 'medium',
            'hint': 'Use the STAR method: Situation, Task, Action, Result'
        },
        {
            'text': 'Describe a project where you had to learn a new technology quickly. What was your approach?',
            'category': 'behavioral',
            'field': 'general',
            'level': 'intermediate',
            'difficulty': 'medium',
            'hint': 'Focus on your learning process and outcomes'
        },
        {
            'text': 'Give me an example of a time when you failed. What did you learn from it?',
            'category': 'behavioral',
            'field': 'general',
            'level': 'entry',
            'difficulty': 'medium',
            'hint': 'Show accountability and growth mindset'
        },
        {
            'text': 'Why do you want to work for our company?',
            'category': 'hr',
            'field': 'general',
            'level': 'entry',
            'difficulty': 'easy',
            'hint': 'Research the company and align with their values'
        },
        {
            'text': 'Where do you see yourself in 5 years?',
            'category': 'hr',
            'field': 'general',
            'level': 'entry',
            'difficulty': 'easy',
            'hint': 'Show ambition while being realistic'
        },
        {
            'text': 'What is your greatest strength and weakness?',
            'category': 'hr',
            'field': 'general',
            'level': 'entry',
            'difficulty': 'easy',
            'hint': 'Be honest and show how you are working on your weakness'
        },
    ]
    
    for q in questions:
        cursor.execute('''
            INSERT INTO questions (uuid, text, category, field, level, difficulty, hint)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            str(uuid.uuid4()),
            q['text'],
            q['category'],
            q['field'],
            q['level'],
            q['difficulty'],
            q['hint']
        ))
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ DATABASE SETUP COMPLETE!")
    print(f"📁 Location: {os.path.abspath(DB_PATH)}")
    print(f"📊 Tables: users, interviews, questions, answers, feedback")
    print(f"📝 Sample questions: {len(questions)}")
    print(f"\n🚀 You can now run: python app.py")

if __name__ == '__main__':
    create_database()