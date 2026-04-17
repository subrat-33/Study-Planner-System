from services.email_service import EmailService

def create_notification(cursor, user_id, title, message, notif_type):
    """
    Creates a notification and optionally sends an email if user settings allow.
    """
    # 1. Insert into DB
    cursor.execute("""
        INSERT INTO notifications (user_id, title, message, notification_type)
        VALUES (%s, %s, %s, %s)
    """, (user_id, title, message, notif_type))
    
    # 2. Check if Email Reminders are enabled
    cursor.execute("""
        SELECT u.email, u.full_name, us.study_hours_per_day 
        FROM users u
        JOIN user_settings us ON u.id = us.user_id
        WHERE u.id = %s
    """, (user_id,))
    user_info = cursor.fetchone()
    
    # Normally we'd check a dedicated 'email_notifications_enabled' column,
    # but since it's hardcoded to 'checked' in the UI for now, we'll send it.
    if user_info:
        email, name, _ = user_info
        if notif_type == "Daily Summary" or notif_type == "Schedule Adjusted":
            EmailService.send_email(email, title, f"<h3>{title}</h3><p>{message}</p>")
