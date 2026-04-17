from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import mysql.connector
from config import Config

user_bp = Blueprint('user', __name__)

def get_db_connection():
    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE
    )

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id, username, email, full_name, profile_picture_url FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        if not user:
            return jsonify({"message": "User not found"}), 404
        return jsonify(user), 200
    finally:
        cursor.close()
        conn.close()

@user_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE users SET full_name = %s, profile_picture_url = %s WHERE id = %s", 
            (data['full_name'], data.get('profile_picture_url'), user_id)
        )
        conn.commit()
        return jsonify({"message": "Profile updated"}), 200
    finally:
        cursor.close()
        conn.close()

@user_bp.route('/settings', methods=['GET'])
@jwt_required()
def get_settings():
    user_id = get_jwt_identity()
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM user_settings WHERE user_id = %s", (user_id,))
        settings = cursor.fetchone()
        return jsonify(settings), 200
    finally:
        cursor.close()
        conn.close()

@user_bp.route('/settings', methods=['PUT'])
@jwt_required()
def update_settings():
    user_id = get_jwt_identity()
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE user_settings SET 
            study_hours_per_day = %s, study_start_time = %s, study_end_time = %s, 
            learning_style = %s, break_duration_minutes = %s 
            WHERE user_id = %s
        """, (
            data.get('study_hours_per_day'), data.get('study_start_time'), data.get('study_end_time'),
            data.get('learning_style'), data.get('break_duration_minutes'), user_id
        ))
        conn.commit()
        return jsonify({"message": "Settings updated"}), 200
    finally:
        cursor.close()
        conn.close()
