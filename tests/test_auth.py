import unittest
import json
from flask import Flask
from flask_testing import TestCase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import Base, User, app 


engine = create_engine('sqlite:///:memory:', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

class TestAuth(TestCase):
    def create_app(self):
        # Configure the Flask app for testing
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        # Create a session and add some test data
        self.session = Session()
        self.client = app.test_client()

        # Add test users
        self.user1 = User(username='testuser1', email='testuser1@example.com', password='password1')
        self.user2 = User(username='testuser2', email='testuser2@example.com', password='password2')
        self.session.add_all([self.user1, self.user2])
        self.session.commit()

    def tearDown(self):
        # Remove the test data and close the session
        self.session.remove()
        self.session.close()

    def test_register(self):
        # Test successful registration
        data = {'username': 'newuser', 'email': 'newuser@example.com', 'password': 'newpassword'}
        response = self.client.post('/register', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data)['message'], 'User registered successfully')

        # Test registration with existing username
        data = {'username': 'testuser1', 'email': 'newemail@example.com', 'password': 'newpassword'}
        response = self.client.post('/register', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data)['error'], 'Username or email already exists')

    def test_login(self):
        # Test successful login
        data = {'email': 'testuser1@example.com', 'password': 'password1'}
        response = self.client.post('/login', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['message'], 'Login successful')

        # Test login with invalid credentials
        data = {'email': 'testuser1@example.com', 'password': 'wrongpassword'}
        response = self.client.post('/login', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.data)['error'], 'Invalid email or password')

if __name__ == '__main__':
    unittest.main()