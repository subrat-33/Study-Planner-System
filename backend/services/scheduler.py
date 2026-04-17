import math
from datetime import datetime, timedelta

class StudyScheduler:
    def __init__(self, user_settings, subjects, topics):
        self.settings = user_settings
        self.subjects = {s['id']: s for s in subjects}
        self.topics = topics
        self.daily_hours = float(user_settings['study_hours_per_day'])
        self.start_time = user_settings['study_start_time'] # e.g., "09:00:00"
        
    def calculate_priority(self, topic):
        subject = self.subjects.get(topic['subject_id'])
        if not subject: return 0
        
        # Difficulty Multiplier
        diff_map = {"Easy": 1.0, "Medium": 1.5, "Hard": 2.0}
        mult = diff_map.get(topic.get('difficulty') or subject['difficulty'], 1.5)
        
        # Days Remaining
        deadline = subject['deadline']
        if isinstance(deadline, str):
            deadline = datetime.strptime(deadline.split('T')[0], '%Y-%m-%d').date()
        elif isinstance(deadline, datetime):
            deadline = deadline.date()
        # if it's already a date object, we're good
        
        today = datetime.now().date()
        days_left = (deadline - today).days
        days_left = max(days_left, 1) # Prevent division by zero and treat overdue as urgent
        
        # Base Score (Intensity)
        # We multiply by a large constant to make deadlines more influential than small hour variations
        score = (mult * float(topic['estimated_hours'])) / days_left
        
        # Priority Multiplier
        prio_map = {"High": 1.3, "Medium": 1.0, "Low": 0.7}
        score *= prio_map.get(topic.get('priority', 'Medium'), 1.0)
        
        return score

    def generate_schedule(self):
        # 1. Score all topics
        for topic in self.topics:
            topic['priority_score'] = self.calculate_priority(topic)
            
        # 2. Sort by score
        sorted_topics = sorted(self.topics, key=lambda x: x['priority_score'], reverse=True)
        
        schedule = []
        current_date = datetime.now()
        
        # We'll plan for the next 90 days or until all topics are scheduled
        for day_offset in range(90):
            target_date = current_date + timedelta(days=day_offset)
            available_minutes = self.daily_hours * 60
            current_time = datetime.combine(target_date.date(), datetime.strptime(str(self.start_time), '%H:%M:%S').time())
            
            day_topics = []
            
            # 3. Try to fill the day with highest priority items first
            for topic in sorted_topics:
                if topic.get('scheduled'): continue
                
                topic_hours = float(topic['estimated_hours'])
                # Calculate how much we can do today
                hours_to_do = min(topic_hours, available_minutes / 60)
                
                if hours_to_do >= 0.5: # Only schedule if at least 30 mins left
                    end_time = current_time + timedelta(hours=hours_to_do)
                    item = {
                        "subject_id": topic['subject_id'],
                        "topic_id": topic['id'],
                        "subject_name": self.subjects[topic['subject_id']]['name'],
                        "topic_name": topic['name'],
                        "date": target_date.strftime('%Y-%m-%d'),
                        "start_time": current_time.strftime('%H:%M:%S'),
                        "end_time": end_time.strftime('%H:%M:%S'),
                        "duration": round(hours_to_do, 1),
                        "color": self.subjects[topic['subject_id']].get('color', '#4F46E5')
                    }
                    
                    schedule.append(item)
                    
                    # Track progress on the topic
                    topic['estimated_hours'] = float(topic['estimated_hours']) - hours_to_do
                    if topic['estimated_hours'] <= 0.1: # Consider done if less than 6 mins left
                        topic['scheduled'] = True
                    
                    available_minutes -= (hours_to_do * 60)
                    current_time = end_time
                    
                    # Add a small break if there's still time in the day
                    if available_minutes > 15:
                        break_min = self.settings.get('break_duration_minutes', 15)
                        current_time += timedelta(minutes=break_min)
                        available_minutes -= break_min

            if not any(not t.get('scheduled') for t in sorted_topics):
                break
                
        return schedule
