from flask import Blueprint, jsonify

landing = Blueprint('landing', __name__) # declare our endpoint

@landing.route('/get_completed_quiz', methods=['GET'])
def getCompletedQuizes():
    return jsonify({"name":["Easy Invasive Species Quiz"]}), 200