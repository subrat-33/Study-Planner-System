from datetime import datetime, timedelta
import json
from .scheduler import StudyScheduler
from services.notification_service import create_notification

class AdaptiveRescheduler:
    def __init__(self, user_id, db_conn):
        self.user_id = user_id
        self.conn = db_conn
        self.cursor = db_conn.cursor(dictionary=True)

    def detect_missed_tasks(self):
        """Finds tasks that were scheduled before now but aren't Completed."""
        now = datetime.now()
        today = now.strftime('%Y-%m-%d')
        
        self.cursor.execute("""
            SELECT si.*, t.name as topic_name, s.name as subject_name
            FROM schedule_items si
            JOIN schedules sc ON si.schedule_id = sc.id
            JOIN topics t ON si.topic_id = t.id
            JOIN subjects s ON si.subject_id = s.id
            WHERE sc.user_id = %s AND sc.status = 'Active'
            AND si.schedule_date < %s AND si.status = 'Pending'
            AND s.deadline >= CURDATE()
        """, (self.user_id, today))
        
        return self.cursor.fetchall()

    def run_reschedule(self):
        """Automatically adjusts the schedule based on missed tasks."""
        missed = self.detect_missed_tasks()
        if not missed:
            return None # Nothing to reschedule

        # 1. Get User Data for Scheduler
        self.cursor.execute("SELECT * FROM user_settings WHERE user_id = %s", (self.user_id,))
        settings = self.cursor.fetchone()
        
        self.cursor.execute("SELECT * FROM subjects WHERE user_id = %s AND deadline >= CURDATE()", (self.user_id,))
        subjects = self.cursor.fetchall()
        
        # All topics that are NOT completed yet from active subjects
        self.cursor.execute("""
            SELECT t.* FROM topics t 
            JOIN subjects s ON t.subject_id = s.id 
            WHERE s.user_id = %s AND t.status != 'Completed' AND s.deadline >= CURDATE()
        """, (self.user_id,))
        topics = self.cursor.fetchall()

        # 2. Use the standard scheduler to regenerate from today onwards
        scheduler = StudyScheduler(settings, subjects, topics)
        new_schedule_data = scheduler.generate_schedule()

        # 3. Update Database (same logic as initial generation)
        self.cursor.execute("UPDATE schedules SET status = 'Superseded' WHERE user_id = %s AND status = 'Active'", (self.user_id,))
        
        self.cursor.execute(
            "INSERT INTO schedules (user_id, schedule_json, total_hours_planned) VALUES (%s, %s, %s)",
            (self.user_id, json.dumps(new_schedule_data), sum(float(item['duration']) for item in new_schedule_data))
        )
        new_schedule_id = self.cursor.lastrowid
        
        for item in new_schedule_data:
            self.cursor.execute("""
                INSERT INTO schedule_items 
                (schedule_id, user_id, subject_id, topic_id, day_of_week, schedule_date, start_time, end_time, duration_hours)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                new_schedule_id, 
                self.user_id,
                item['subject_id'], 
                item['topic_id'], 
                datetime.strptime(item['date'], '%Y-%m-%d').weekday(),
                item['date'],
                item['start_time'],
                item['end_time'],
                item['duration']
            ))

        # Log to Rescheduling History
        self.cursor.execute(
            "INSERT INTO rescheduling_history (user_id, new_schedule_id, reason, status) VALUES (%s, %s, %s, %s)",
            (self.user_id, new_schedule_id, f"Auto-rescheduled {len(missed)} missed tasks", 'Accepted')
        )
        
        # Add Notification for user
        create_notification(self.cursor, self.user_id, "Schedule Adjusted", 
                          f"I've updated your plan because {len(missed)} tasks were missed yesterday.", 
                          "Schedule Adjusted")

        self.conn.commit()
        return new_schedule_data
