from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
import bcrypt
import mysql.connector
from config import Config
from services.notification_service import create_notification

auth_bp = Blueprint('auth', __name__)

def get_db_connection():
    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE
    )

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')
    
    if not all([full_name, email, password]):
        return jsonify({"message": "Missing required fields"}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    username = email.split('@')[0] # Simple username generator

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Check if user exists
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({"message": "Email already registered"}), 400

        # Insert user
        cursor.execute(
            "INSERT INTO users (username, email, password_hash, full_name) VALUES (%s, %s, %s, %s)",
            (username, email, hashed_password, full_name)
        )
        user_id = cursor.lastrowid
        
        # Create default settings
        cursor.execute("INSERT INTO user_settings (user_id) VALUES (%s)", (user_id,))
        
        # Add Welcome Notification
        create_notification(cursor, user_id, "Welcome to StudySmart!", 
                          "We're excited to help you achieve your study goals. Start by adding your subjects!", 
                          "Daily Summary")

        conn.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({"message": "Email and password are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            access_token = create_access_token(identity=user['id'])
            return jsonify({
                "access_token": access_token,
                "user": {
                    "id": user['id'],
                    "full_name": user['full_name'],
                    "email": user['email'],
                    "profile_picture_url": user.get('profile_picture_url')
                }
            }), 200
        else:
            return jsonify({"message": "Invalid email or password"}), 401
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
