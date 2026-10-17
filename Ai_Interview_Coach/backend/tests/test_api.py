"""
Test Suite for AI Interview Coach Enterprise Backend
Validates all authentication, interview lifecycle, questions, answers, and analytics endpoints.
"""

import os
import sys
import pytest

# Ensure backend root is on Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db, User, Question, Interview


@pytest.fixture(scope='session')
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['JWT_SECRET_KEY'] = 'test-jwt-super-secret-key-that-is-at-least-32-bytes-long!'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as test_client:
        with app.app_context():
            db.create_all()
            # Seed test question
            q = Question(
                text='Explain the difference between let, const, and var in JavaScript.',
                category='technical',
                field='software',
                level='intermediate',
                difficulty='medium',
                is_verified=True
            )
            db.session.add(q)
            db.session.commit()
            
        yield test_client
        
        with app.app_context():
            db.drop_all()


def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'version' in data


def test_auth_workflow(client):
    # 1. Register
    register_payload = {
        'email': 'jane.doe@example.com',
        'password': 'Password123!',
        'firstName': 'Jane',
        'lastName': 'Doe'
    }
    reg_res = client.post('/api/auth/register', json=register_payload)
    assert reg_res.status_code == 201
    reg_data = reg_res.get_json()
    assert 'token' in reg_data
    token = reg_data['token']
    assert reg_data['user']['email'] == 'jane.doe@example.com'

    # 2. Duplicate registration should fail
    dup_res = client.post('/api/auth/register', json=register_payload)
    assert dup_res.status_code == 409

    # 3. Login
    login_payload = {
        'email': 'jane.doe@example.com',
        'password': 'Password123!'
    }
    log_res = client.post('/api/auth/login', json=login_payload)
    assert log_res.status_code == 200
    log_data = log_res.get_json()
    assert 'token' in log_data

    # 4. Get Current User profile
    headers = {'Authorization': f'Bearer {token}'}
    me_res = client.get('/api/auth/me', headers=headers)
    assert me_res.status_code == 200
    me_data = me_res.get_json()
    assert me_data['user']['email'] == 'jane.doe@example.com'


def test_questions_endpoints(client):
    # Random question
    rand_res = client.post('/api/questions/random', json={'category': 'technical', 'field': 'software'})
    assert rand_res.status_code == 200
    rand_data = rand_res.get_json()
    assert 'question' in rand_data
    assert 'text' in rand_data['question']

    # Question list
    list_res = client.get('/api/questions')
    assert list_res.status_code == 200
    list_data = list_res.get_json()
    assert 'questions' in list_data
    assert len(list_data['questions']) >= 1


def test_interview_lifecycle(client):
    # Register/login user for interview testing
    reg_payload = {
        'email': 'candidate@example.com',
        'password': 'SecretPassword123',
        'firstName': 'Alex',
        'lastName': 'Smith'
    }
    reg_res = client.post('/api/auth/register', json=reg_payload)
    token = reg_res.get_json()['token']
    headers = {'Authorization': f'Bearer {token}'}

    # 1. Start Interview
    start_payload = {
        'field': 'software',
        'level': 'intermediate',
        'type': 'technical',
        'mode': 'text',
        'questionsTotal': 3
    }
    start_res = client.post('/api/interviews/start', json=start_payload, headers=headers)
    assert start_res.status_code == 201
    start_data = start_res.get_json()
    interview_uuid = start_data['interview']['id']

    # 2. Submit Answer
    answer_payload = {
        'interviewId': interview_uuid,
        'questionText': 'Explain the difference between let, const, and var in JavaScript.',
        'answer': 'var has function scope and is hoisted. let and const have block scope and live in the temporal dead zone. const cannot be reassigned once declared, whereas let can. In modern ES6 development, const is preferred by default and let when reassignment is required.',
        'timeSpent': 45
    }
    ans_res = client.post('/api/answers/submit', json=answer_payload, headers=headers)
    assert ans_res.status_code == 200
    ans_data = ans_res.get_json()
    assert 'feedback' in ans_data
    assert ans_data['feedback']['score'] >= 5.0
    assert len(ans_data['feedback']['strengths']) > 0

    # 3. Complete Interview
    complete_payload = {
        'duration': 180,
        'score': 8.5,
        'questionsAnswered': 1
    }
    comp_res = client.post(f'/api/interviews/{interview_uuid}/complete', json=complete_payload, headers=headers)
    assert comp_res.status_code == 200
    comp_data = comp_res.get_json()
    assert comp_data['interview']['status'] == 'completed'

    # 4. Analytics Overview
    overview_res = client.get('/api/analytics/overview', headers=headers)
    assert overview_res.status_code == 200
    ov_data = overview_res.get_json()
    assert ov_data['totalInterviews'] >= 1

    # 5. Performance Timeline
    perf_res = client.get('/api/analytics/performance', headers=headers)
    assert perf_res.status_code == 200
    perf_data = perf_res.get_json()
    assert 'performanceData' in perf_data


def test_leaderboard_and_stats(client):
    lb_res = client.get('/api/leaderboard')
    assert lb_res.status_code == 200
    assert 'leaderboard' in lb_res.get_json()

    stats_res = client.get('/api/admin/stats')
    assert stats_res.status_code == 200
    stats_data = stats_res.get_json()
    assert stats_data['status'] == 'operational'
