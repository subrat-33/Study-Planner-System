import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config

class EmailService:
    @staticmethod
    def send_email(to_email, subject, body):
        """
        Sends an email using SMTP. 
        Note: Requires SMTP configuration in Config.
        """
        # For now, we'll log it to console as well
        print(f"--- MOCK EMAIL SENT TO {to_email} ---")
        print(f"Subject: {subject}")
        print(f"Body: {body}")
        print("---------------------------------------")

        # Basic implementation (would need valid credentials)
        # try:
        #     msg = MIMEMultipart()
        #     msg['From'] = 'StudySmart <noreply@studysmart.com>'
        #     msg['To'] = to_email
        #     msg['Subject'] = subject
        #     msg.attach(MIMEText(body, 'html'))
        #     
        #     # Example for Gmail:
        #     # server = smtplib.SMTP('smtp.gmail.com', 587)
        #     # server.starttls()
        #     # server.login('your-email@gmail.com', 'your-app-password')
        #     # server.send_message(msg)
        #     # server.quit()
        # except Exception as e:
        #     print(f"Failed to send email: {e}")

    @staticmethod
    def send_daily_summary(user_email, user_name, tasks_count):
        subject = f"Your Daily Study Summary - {user_name}"
        body = f"""
        <html>
        <body>
            <h2>Hello {user_name}!</h2>
            <p>You have <b>{tasks_count}</b> study sessions planned for today.</p>
            <p>Consistency is key to success. Good luck with your studies!</p>
            <br>
            <p>Best regards,<br>StudySmart Team</p>
        </body>
        </html>
        """
        EmailService.send_email(user_email, subject, body)
