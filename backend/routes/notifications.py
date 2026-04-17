from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import mysql.connector
from config import Config

notifications_bp = Blueprint('notifications', __name__)

def get_db_connection():
    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE
    )

@notifications_bp.route('/', methods=['GET'])
@jwt_required()
def get_notifications():
    user_id = get_jwt_identity()
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM notifications WHERE user_id = %s ORDER BY created_at DESC LIMIT 20", (user_id,))
        notifications = cursor.fetchall()
        return jsonify(notifications), 200
    finally:
        cursor.close()
        conn.close()

@notifications_bp.route('/unread-count', methods=['GET'])
@jwt_required()
def get_unread_count():
    user_id = get_jwt_identity()
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT COUNT(*) as count FROM notifications WHERE user_id = %s AND is_read = FALSE", (user_id,))
        result = cursor.fetchone()
        return jsonify(result), 200
    finally:
        cursor.close()
        conn.close()

@notifications_bp.route('/total-count', methods=['GET'])
@jwt_required()
def get_total_count():
    user_id = get_jwt_identity()
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT COUNT(*) as count FROM notifications WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        return jsonify(result), 200
    finally:
        cursor.close()
        conn.close()

@notifications_bp.route('/mark-as-read', methods=['POST'])
@jwt_required()
def mark_as_read():
    user_id = get_jwt_identity()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("UPDATE notifications SET is_read = TRUE WHERE user_id = %s", (user_id,))
        conn.commit()
        return jsonify({"message": "Notifications marked as read"}), 200
    finally:
        cursor.close()
        conn.close()
