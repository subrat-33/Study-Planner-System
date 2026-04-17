from flask import Flask, jsonify, render_template
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
import os

def create_app():
    app = Flask(__name__, 
                template_folder='../frontend/templates',
                static_folder='../frontend/static')
    app.config.from_object(Config)
    
    CORS(app)
    jwt = JWTManager(app)
    
    app.config['UPLOAD_FOLDER'] = os.path.join(app.static_folder, 'uploads')
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    # Frontend Routes
    @app.route('/')
    def index(): return render_template('index.html')
    
    @app.route('/login')
    def login(): return render_template('login.html')
    
    @app.route('/register')
    def register(): return render_template('register.html')
    
    @app.route('/dashboard')
    def dashboard(): return render_template('dashboard.html')
    
    @app.route('/subjects')
    def subjects(): return render_template('subjects.html')
    
    @app.route('/schedule')
    def schedule(): return render_template('schedule.html')
    
    @app.route('/progress')
    def progress(): return render_template('progress.html')
    
    @app.route('/analytics')
    def analytics(): return render_template('analytics.html')
    
    @app.route('/settings')
    def settings(): return render_template('settings.html')

    @app.route('/notifications')
    def notifications(): return render_template('notifications.html')

    @app.route('/help')
    def help(): return render_template('help.html')

    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "healthy", "message": "Smart Study Planner API is running"}), 200

    # Register blueprints
    from routes.auth import auth_bp
    from routes.subjects import subjects_bp
    from routes.schedule import schedule_bp
    from routes.progress import progress_bp
    from routes.user import user_bp
    from routes.notifications import notifications_bp
    from routes.upload import upload_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(subjects_bp, url_prefix='/api/subjects')
    app.register_blueprint(schedule_bp, url_prefix='/api/schedule')
    app.register_blueprint(progress_bp, url_prefix='/api/progress')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(notifications_bp, url_prefix='/api/notifications')
    app.register_blueprint(upload_bp, url_prefix='/api/upload')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000, host='0.0.0.0')
