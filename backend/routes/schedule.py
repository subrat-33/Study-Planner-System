from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import mysql.connector
import json
from config import Config
from datetime import datetime
from services.scheduler import StudyScheduler
from services.notification_service import create_notification

schedule_bp = Blueprint('schedule', __name__)

def get_db_connection():
    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE
    )

@schedule_bp.route('/generate', methods=['POST'])
@jwt_required()
def generate():
    user_id = get_jwt_identity()
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # 1. Get User Settings
        cursor.execute("SELECT * FROM user_settings WHERE user_id = %s", (user_id,))
        settings = cursor.fetchone()
        
        # 2. Get Subjects (Only those whose exams are not over)
        cursor.execute("SELECT * FROM subjects WHERE user_id = %s AND deadline >= CURDATE()", (user_id,))
        subjects = cursor.fetchall()
        
        # 3. Get Topics (only pending ones from active subjects)
        cursor.execute("""
            SELECT t.* FROM topics t 
            JOIN subjects s ON t.subject_id = s.id 
            WHERE s.user_id = %s AND t.status != 'Completed' AND s.deadline >= CURDATE()
        """, (user_id,))
        topics = cursor.fetchall()
        
        if not subjects or not topics:
            return jsonify({"message": "Add subjects and topics first"}), 400

        # 4. Run Scheduler
        scheduler = StudyScheduler(settings, subjects, topics)
        new_schedule_data = scheduler.generate_schedule()
        
        # 5. Save to Database
        # Archive old active schedule
        cursor.execute("UPDATE schedules SET status = 'Superseded' WHERE user_id = %s AND status = 'Active'", (user_id,))
        
        # Insert new schedule
        cursor.execute(
            "INSERT INTO schedules (user_id, schedule_json, total_hours_planned) VALUES (%s, %s, %s)",
            (user_id, json.dumps(new_schedule_data), sum(float(item['duration']) for item in new_schedule_data))
        )
        schedule_id = cursor.lastrowid
        
        # Insert schedule items for easy querying
        for item in new_schedule_data:
            cursor.execute("""
                INSERT INTO schedule_items 
                (schedule_id, user_id, subject_id, topic_id, day_of_week, schedule_date, start_time, end_time, duration_hours)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                schedule_id, 
                user_id,
                item['subject_id'], 
                item['topic_id'], 
                datetime.strptime(item['date'], '%Y-%m-%d').weekday(),
                item['date'],
                item['start_time'],
                item['end_time'],
                item['duration']
            ))
            
        # Add Notification
        create_notification(cursor, user_id, "Schedule Generated", 
                          f"Your optimized study plan with {len(new_schedule_data)} slots is ready!", 
                          "Schedule Adjusted")

        conn.commit()
        return jsonify({"message": "Schedule generated successfully", "count": len(new_schedule_data)}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@schedule_bp.route('', methods=['GET'])
@jwt_required()
def get_current_schedule():
    user_id = get_jwt_identity()
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT schedule_json FROM schedules WHERE user_id = %s AND status = 'Active' ORDER BY created_at DESC LIMIT 1", (user_id,))
        row = cursor.fetchone()
        if row:
            return jsonify(json.loads(row['schedule_json'])), 200
        return jsonify([]), 200
    finally:
        cursor.close()
        conn.close()

from services.reschedule import AdaptiveRescheduler

@schedule_bp.route('/reschedule', methods=['POST'])
@jwt_required()
def adaptive_reschedule():
    user_id = get_jwt_identity()
    conn = get_db_connection()
    try:
        rescheduler = AdaptiveRescheduler(user_id, conn)
        new_schedule = rescheduler.run_reschedule()
        if new_schedule:
            return jsonify({"message": "Schedule adjusted for missed tasks", "data": new_schedule}), 200
        return jsonify({"message": "Schedule is already up to date"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    finally:
        conn.close()
