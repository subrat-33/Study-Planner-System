from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import mysql.connector
from config import Config
from datetime import datetime

progress_bp = Blueprint('progress', __name__)

def get_db_connection():
    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE
    )

@progress_bp.route('/summary', methods=['GET'])
@jwt_required()
def get_summary():
    user_id = get_jwt_identity()
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Today's Tasks
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute("""
            SELECT COUNT(*) as count 
            FROM schedule_items si
            JOIN schedules s ON si.schedule_id = s.id
            WHERE s.user_id = %s AND si.schedule_date = %s AND si.status = 'Pending'
        """, (user_id, today))
        today_tasks = cursor.fetchone()['count']
        
        # Overall Progress
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) as completed
            FROM topics t
            JOIN subjects s ON t.subject_id = s.id
            WHERE s.user_id = %s
        """, (user_id,))
        prog_data = cursor.fetchone()
        overall_progress = round((prog_data['completed'] / prog_data['total'] * 100)) if prog_data['total'] > 0 else 0
        
        # Next Upcoming Deadline (only future exams)
        cursor.execute("SELECT MIN(deadline) as next_deadline FROM subjects WHERE user_id = %s AND deadline >= CURDATE()", (user_id,))
        deadline_row = cursor.fetchone()
        days_left = None
        if deadline_row and deadline_row['next_deadline']:
            days_left = (deadline_row['next_deadline'] - datetime.now().date()).days

        return jsonify({
            "today_tasks": today_tasks,
            "overall_progress": overall_progress,
            "days_until_exam": days_left
        }), 200
    finally:
        cursor.close()
        conn.close()

@progress_bp.route('/<int:topic_id>', methods=['PUT'])
@jwt_required()
def update_progress(topic_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    status = data.get('status')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if progress record exists
        cursor.execute("SELECT id FROM progress WHERE user_id = %s AND topic_id = %s", (user_id, topic_id))
        row = cursor.fetchone()
        
        if row:
            cursor.execute(
                "UPDATE progress SET status = %s, completed_at = %s WHERE id = %s",
                (status, datetime.now() if status == 'Completed' else None, row[0])
            )
        else:
            cursor.execute(
                "INSERT INTO progress (user_id, topic_id, status, completed_at) VALUES (%s, %s, %s, %s)",
                (user_id, topic_id, status, datetime.now() if status == 'Completed' else None)
            )
        
        # Update topic status as well
        cursor.execute("UPDATE topics SET status = %s WHERE id = %s", (status, topic_id))
        
        # Mark schedule item as completed if it exists
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute("""
            UPDATE schedule_items 
            SET status = 'Completed' 
            WHERE topic_id = %s AND schedule_date = %s
        """, (topic_id, today))
        
        if status == 'Completed':
            # Get topic name for the notification
            cursor.execute("SELECT name FROM topics WHERE id = %s", (topic_id,))
            topic_name = cursor.fetchone()[0]
            cursor.execute("""
                INSERT INTO notifications (user_id, title, message, notification_type)
                VALUES (%s, %s, %s, %s)
            """, (user_id, "Well Done! 🎉", f"You've completed '{topic_name}'. Keep up the great momentum!", "Daily Summary"))

        conn.commit()
        return jsonify({"message": "Progress updated"}), 200
    finally:
        cursor.close()
        conn.close()

@progress_bp.route('/analytics', methods=['GET'])
@jwt_required()
def get_analytics():
    user_id = get_jwt_identity()
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Get basic stats
        cursor.execute("""
            SELECT 
                COUNT(*) as total_topics,
                SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) as completed_topics
            FROM topics t
            JOIN subjects s ON t.subject_id = s.id
            WHERE s.user_id = %s
        """, (user_id,))
        topic_stats = cursor.fetchone()
        
        # Trend Data (Last 7 days)
        # For simplicity, we'll return some aggregated data or placeholders
        # In a full app, we'd query schedule_items status change history
        
        # Subject Distribution
        cursor.execute("""
            SELECT name, 
            (SELECT COUNT(*) FROM topics WHERE subject_id = s.id) as topic_count,
            (SELECT COUNT(*) FROM topics WHERE subject_id = s.id AND status = 'Completed') as completed_count
            FROM subjects s WHERE user_id = %s
        """, (user_id,))
        subjects = cursor.fetchall()
        
        return jsonify({
            "total_hours": 24, # Placeholder
            "avg_hours": 3.5,
            "streak": 5,
            "completion_rate": round((topic_stats['completed_topics'] / topic_stats['total_topics'] * 100)) if topic_stats['total_topics'] > 0 else 0,
            "subj_labels": [s['name'] for s in subjects],
            "subj_data": [s['topic_count'] for s in subjects],
            "completed_topics": [s['completed_count'] for s in subjects],
            "remaining_topics": [s['topic_count'] - s['completed_count'] for s in subjects]
        }), 200
    finally:
        cursor.close()
        conn.close()
