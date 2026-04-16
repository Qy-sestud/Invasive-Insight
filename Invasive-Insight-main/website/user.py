from flask import Blueprint, jsonify, request
from .models import User, db
from datetime import datetime

user = Blueprint('user', __name__) # creates a user Blueprint to organize user-related actions

#method to update user's profile
@user.route('/update_profile/<int:user_id>', methods=['PUT']) # 'PUT' request commonly used to update resources
def update_profile(user_id):
    # Find the user by ID
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Get the JSON data from the request
    data = request.get_json()

    # Update user fields if provided
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        # Check if email is unique
        if User.query.filter_by(email=data['email']).first():
            return jsonify({"error": "Email already exists"}), 400
        user.email = data['email']
    if 'password' in data:
        user.password = data['password']

    try:
        db.session.commit()
        return jsonify({"message": "Profile updated successfully"}), 200
    except Exception as e:
        db.session.rollback()  # Roll back the session in case of an error
        return jsonify({"error": str(e)}), 500


#method to submit a user's score and quiz complete time
@user.route('/users/<int:user_id>/score_time', methods=['POST'])
def submit_user_score_time(user_id):
    try:
        # Fetch the user by ID
        user = User.query.get(user_id)
        if not user:
            return jsonify({"status": "error", "message": "User not found"}), 404

        # Parse the JSON payload
        data = request.get_json()
        if not data or "score" not in data:
            return jsonify({"status": "error", "message": "Score is required"}), 400

        # Validate the score
        new_score = data["score"]
        if not isinstance(new_score, int) or new_score < 0:
            return jsonify({"status": "error", "message": "Score must be a non-negative integer"}), 400

        # Update the user's score
        user.score = new_score

        # Update the user's completion time if the score is submitted
        if "completed_at" in data and data["completed_at"]:
            # Use the provided completion time (if sent in request payload)
            user.completed_at = datetime.fromisoformat(data["completed_at"])
        else:
            # Otherwise, use the current time as the completion time
            user.completed_at = datetime.now()

        # Commit changes to the database
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Score and completion time updated successfully",
            "data": {"user_id": user.user_id, "new_score": new_score, "completed_at": user.completed_at.isoformat()}
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    

#method to get a user's score
@user.route('/users/<int:user_id>/score', methods=['GET'])
def get_user_score(user_id):
    """Retrieve a specific user's score."""
    try:
        # Fetch the user by ID
        user = User.query.get(user_id)
        if not user:
            return jsonify({"status": "error", "message": "User not found"}), 404

        return jsonify({            
            "data": {
                "user_id": user.user_id,
                "username": user.username,
                "score": user.score
            }
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500