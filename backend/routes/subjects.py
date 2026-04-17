from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import mysql.connector
from config import Config
from services.notification_service import create_notification

subjects_bp = Blueprint('subjects', __name__)

def get_db_connection():
    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE
    )

@subjects_bp.route('', methods=['GET'])
@jwt_required()
def get_subjects():
    user_id = get_jwt_identity()
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            SELECT s.*, 
            (SELECT COALESCE(AVG(p.status = 'Completed') * 100, 0) 
             FROM topics t 
             LEFT JOIN progress p ON t.id = p.topic_id 
             WHERE t.subject_id = s.id) as progress
            FROM subjects s WHERE s.user_id = %s
        """, (user_id,))
        subjects = cursor.fetchall()
        # Convert Decimals to floats for JSON serialization
        for s in subjects:
            if 'progress' in s and s['progress'] is not None:
                s['progress'] = float(s['progress'])
            if 'weekly_hours' in s and s['weekly_hours'] is not None:
                s['weekly_hours'] = float(s['weekly_hours'])
                
        return jsonify(subjects), 200
    finally:
        cursor.close()
        conn.close()

@subjects_bp.route('', methods=['POST'])
@jwt_required()
def add_subject():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO subjects (user_id, name, difficulty, deadline, weekly_hours, description) VALUES (%s, %s, %s, %s, %s, %s)",
            (user_id, data['name'], data['difficulty'], data['deadline'], data['weekly_hours'], data.get('description'))
        )
        
        # Add Notification
        create_notification(cursor, user_id, "New Subject", 
                          f"Added '{data['name']}' to your planner.", 
                          "Daily Summary")

        conn.commit()
        return jsonify({"message": "Subject added"}), 201
    finally:
        cursor.close()
        conn.close()

@subjects_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_subject(id):
    user_id = get_jwt_identity()
    data = request.get_json()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "UPDATE subjects SET name=%s, difficulty=%s, deadline=%s, weekly_hours=%s, description=%s WHERE id=%s AND user_id=%s",
            (data['name'], data['difficulty'], data['deadline'], data['weekly_hours'], data.get('description'), id, user_id)
        )
        conn.commit()
        return jsonify({"message": "Subject updated"}), 200
    finally:
        cursor.close()
        conn.close()

# Topic Routes
@subjects_bp.route('/<int:subj_id>/topics', methods=['GET'])
@jwt_required()
def get_topics(subj_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM topics WHERE subject_id = %s", (subj_id,))
        topics = cursor.fetchall()
        return jsonify(topics), 200
    finally:
        cursor.close()
        conn.close()

@subjects_bp.route('/<int:subj_id>/topics', methods=['POST'])
@jwt_required()
def add_topic(subj_id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO topics (subject_id, name, estimated_hours, priority) VALUES (%s, %s, %s, %s)",
            (subj_id, data['name'], data['estimated_hours'], data['priority'])
        )
        # Update topic count in subject
        cursor.execute("UPDATE subjects SET total_topics = total_topics + 1 WHERE id = %s", (subj_id,))
        
        # Get user_id and subject name for notification
        cursor.execute("SELECT user_id, name FROM subjects WHERE id = %s", (subj_id,))
        subject_info = cursor.fetchone()
        
        if subject_info:
            create_notification(cursor, subject_info[0], "Topic Added", 
                              f"New topic '{data['name']}' added to {subject_info[1]}.", 
                              "Daily Summary")

        conn.commit()
        return jsonify({"message": "Topic added"}), 201
    finally:
        cursor.close()
        conn.close()

@subjects_bp.route('/<int:subj_id>/topics/<int:topic_id>', methods=['DELETE'])
@jwt_required()
def delete_topic(subj_id, topic_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM topics WHERE id = %s AND subject_id = %s", (topic_id, subj_id))
        cursor.execute("UPDATE subjects SET total_topics = total_topics - 1 WHERE id = %s", (subj_id,))
        conn.commit()
        return jsonify({"message": "Topic deleted"}), 200
    finally:
        cursor.close()
        conn.close()
