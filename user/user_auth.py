from flask import Flask, request, jsonify, session, url_for, redirect
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import bcrypt
import pymysql
from app import app
from user.model import User, Session

def register():
    data = request.get_json()

    # Extract user information from the request data
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Validate data: ensure username, email, and password are provided
    if not username or not email or not password:
        return jsonify({"error": "All fields (username, email, password) are required"}), 400

    # Create a session
    session = Session()

    try:
        existing_user = session.query(User).filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            return jsonify({"error": "Username or email already exists"}), 400
        
        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Create a new user instance
        new_user = User(username=username, email=email, password=hashed_password.decode('utf-8'))
        
        # Add the new user to the session and commit the transaction
        session.add(new_user)
        session.commit()
        
        # Return a success response
        return jsonify({"message": "User registered successfully"}), 201
    
    except Exception as e:
        session.rollback()
        return jsonify({"error": "Internal server error"}), 500
    
    finally:
        session.close()
        

def login():
    data = request.get_json()
    
    # Extract user credentials from the request data
    email = data.get('email')
    password = data.get('password')
    
    # Validate data: ensure both email and password are provided
    if not email or not password:
        return jsonify({"error": "Both email and password are required"}), 400
    
    # Create a session
    session = Session()
    
    try:
        # Query the database for the user with the provided email
        user = session.query(User).filter_by(email=email).first()
        
        if not user:
            return jsonify({"error": "Invalid email or password"}), 401
        
        # Verify the provided password against the stored hashed password
        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return jsonify({"error": "Invalid email or password"}), 401
        
        return jsonify({"message": "Login successful"}), 200
    
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500
    
    finally:
        session.close()
        
        
def logout():
    session.pop("login", None)
    
    return redirect(url_for("login"))