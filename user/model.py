from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import bcrypt
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

pymysql.install_as_MySQLdb()

DB_URI = f"mysql://{os.environ['DB_USERNAME']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"

engine = create_engine(DB_URI)


Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    reset_token = Column(String(255), nullable=True)

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"

Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine) 
