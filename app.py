from flask import Flask, request, jsonify, render_template
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import pymysql  
from user.model import engine, User
from flask_cors import CORS

pymysql.install_as_MySQLdb()

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/')
def index():
    return render_template("docs.html")

@app.route('/register', methods=['POST'])
def register_route():
    from user.user_auth import register

    return register()
        
        
@app.route('/login', methods=['POST'])
def login_route():
    from user.user_auth import login
    
    return login()

@app.route('/forgot-password', methods=['POST'])
def forgot_password_route():
    from user.forgot_password import forgot_password
    
    return forgot_password()

@app.route('/logout')
def logout_route():
    from user.user_auth import logout
    
    return logout