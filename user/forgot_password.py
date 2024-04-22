from flask import Flask, jsonify, request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets
import os
from .model import User, Session

EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

def send_reset_email(email, token):
    subject = 'Password Reset Request'
    body = f'To reset your password, click the following link: http://localhost/5000/forgot-password/reset-password?token={token}'
    
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    text = msg.as_string()
    
    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.sendmail(EMAIL_ADDRESS, email, text)
    server.quit()

def forgot_password():
    data = request.get_json()
    
    # Extract email from the request data
    email = data.get('email')
    
    # Validate data: ensure email is provided
    if not email:
        return jsonify({"error": "Email is required"}), 400
    
    # Create a session
    session = Session()
    
    try:
        # Query the database for the user with the provided email
        user = session.query(User).filter_by(email=email).first()
        
        if not user:
            return jsonify({"error": "No user found with that email"}), 404
        
        # Generate a unique token for password reset
        token = secrets.token_urlsafe(16)
        
        # Save the token to the user's record in the database (you may need to add a token column to your User model)
        user.reset_token = token
        session.commit()
        
        # Send the reset password email
        send_reset_email(email, token)
        
        return jsonify({"message": "Password reset instructions sent to your email"}), 200
    
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500
    
    finally:
        session.close()