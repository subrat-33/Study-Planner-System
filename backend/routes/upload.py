from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
import uuid
from werkzeug.utils import secure_filename

upload_bp = Blueprint('upload', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/profile-pic', methods=['POST'])
@jwt_required()
def upload_profile_pic():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        user_id = get_jwt_identity()
        extension = file.filename.rsplit('.', 1)[1].lower()
        filename = f"user_{user_id}_{uuid.uuid4().hex[:8]}.{extension}"
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        file.save(filepath)
        
        # Return the public URL
        url = f"/static/uploads/{filename}"
        return jsonify({"url": url}), 200
    
    return jsonify({"message": "Invalid file type"}), 400
