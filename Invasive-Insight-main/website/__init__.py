import os
import base64
from flask import Flask, jsonify, request,session, redirect, url_for
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload

DATABASE_NAME = 'invasive_insight.db'
db = SQLAlchemy()

from .models import Question, Quiz, User, Bookmark

def create_app():
    app = Flask(__name__)
    app.secret_key = 'secretkey'
    # enable Cross site origin requests
    CORS(app)

    # Define constants
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_NAME}'

    # Initialize the database object
    db.init_app(app)

    # add all questions into the database automatically
    @app.before_request
    def add_questions():
        """ Automatically adds all quiz questions when app starts, if no questions exist in the database. """
        if Question.query.count() == 0:  # Check if there are no questions in the database

            # Define all 10 questions and their data
            questions_data = [
                {
                'question': 'The fish is an invasive species in Malaysia that has spread throughout the waterways in Malaysia. What is the name of the fish?',
                'options': {
                    'A': "A) Ikan pacu (Mylopus)", 
                    'B': "B) Suckermouth catfish (Hypostomus plecostomus)",
                    'C': "C) African catfish",
                    'D': "D) Flower horn (Cichiasoma)"
                },
                'correct_answer': "B) Suckermouth catfish (Hypostomus plecostomus)",
                'explanation': """This fish is also known as “Ikan Bandaraya” in Malaysia...""",
                'hint': "This fish is black in colour."
                },
                {
                'question': 'Why do the populations of invasive species grow so quickly?',
                'options': {
                    'A': "Invasive species are native to an area.",
                    'B': "Invasive species are prey to many animals.",
                    'C': "Invasive species have no predators.",
                    'D': "Invasive species keep the ecosystems in equilibrium."
                },
                'correct_answer': 'Invasive species have no predators.',
                'explanation': """Invasive species often grow quickly in a new environment because they lack natural predators. In their native habitats, predators, parasites, and diseases help control their populations. However, when these species are introduced to a new area, the local ecosystem often lacks the specific predators or diseases that can limit their growth. This allows invasive species to reproduce rapidly, often outcompeting native species and disrupting the balance of the ecosystem.""",
                'hint': "Think about what controls the population of a species in an ecosystem. What role do predators play in keeping populations in check?"
                },
                {
                'question': 'Apple Snail is one of the invasive species in Malaysia. Why is the Apple Snail considered an invasive species in Malaysia’s wetlands?',
                'options': {
                    'A': "It disrupts rice paddies by feeding on young rice plants",
                    'B': "It reduces fish population by preying on native fish",
                    'C': "It causes water pollution by excreting harmful chemicals",
                    'D': "It assists in mosquito breeding"
                },
                'correct_answer': 'It disrupts rice paddies by feeding on young rice plants',
                'explanation': """Apple Snails feed on young, tender rice plants and other crops, which causes major damage in paddy fields. This results in lower crop yields, increasing costs and labor requirements for farmers who must control the snails.""",
                'hint': "This type of snail is known for its appetite for tender plants. Think about how this could affect crops in wetland areas."
                },
                {
                'question': 'Which of the following is a major consequence of invasive species in Malaysia?',
                'options': {
                    'A': "They help increase biodiversity",
                    'B': "They threaten native species and disrupt ecosystems",
                    'C': "They create more food sources for animals",
                    'D': "They have no real impact"
                },
                'correct_answer': 'They threaten native species and disrupt ecosystems',
                'explanation': """These species often compete with local flora and fauna for resources like food, water, and space, sometimes outcompeting them entirely. Invasive species can disrupt the natural balance of ecosystems by preying on native species, introducing new diseases, and altering habitats, which can lead to the decline or extinction of native species. This disruption affects biodiversity and can lead to broader ecological consequences, such as changes in soil health, water quality, and even the structure of entire ecosystems.""",
                'hint': "Think about the impact that non-native species might have on local plants and animals when they compete for resources like food, water, and space. How might this competition affect the balance of the natural environment?"
                },
                {
                'question': 'Which invasive plant species in Malaysia poses a threat to native plants by spreading rapidly and taking over natural habitats?',
                'options': {
                    'A': "Mangrove Tree",
                    'B': "Oil Palm",
                    'C': "Water Hyacinth",
                    'D': "Rubber Tree"
                },
                'correct_answer': 'Water Hyacinth',
                'explanation': """Water Hyacinth is an invasive aquatic plant that spreads quickly over water surfaces, blocking sunlight and depleting oxygen levels in the water. This growth disrupts the ecosystem, making it difficult for native aquatic plants and fish to survive.""",
                'hint': "It is very light compared to the others."
                },
                {
                'question': 'Why are invasive species a threat to Malaysia’s ecosystems?',
                'options': {
                    'A': "They help control local pest populations",
                    'B': "They contribute to biodiversity by introducing new species",
                    'C': "They often compete with native species for resources",
                    'D': "They enhance soil quality and reduce pollution"
                },
                'correct_answer': 'They often compete with native species for resources',
                'explanation': """The direct threats of invasive species include outcompeting native species for food or other resources, causing or carrying disease, and preventing native species from reproducing or killing a native species' young.""",
                'hint': "Think about how non-native species might impact the resources and survival of species that already live in the ecosystem."
                },
                {
                'question': 'Which of the following is NOT a reason why the Red-Eared Slider turtle is considered an invasive species in Malaysia?',
                'options': {
                    'A': "It competes with native turtles for food and habitat",
                    'B': "It is a natural predator of local pests like mosquitoes",
                    'C': "It spreads diseases that affect native species",
                    'D': "It can outcompete and displace native turtle populations"
                },
                'correct_answer': 'It is a natural predator of local pests like mosquitoes',
                'explanation': """The Red-Eared Slider turtle is considered invasive because it competes with native turtles for resources, spreads diseases, and outcompetes native populations. It is not known for controlling local pests like mosquitoes.""",
                'hint': "Think about the kind of impact the Red-Eared Slider has on the environment. Does it help by eating pests, or does it cause problems for native turtles?"
                },
                {
                'question': 'Which of the following species is considered invasive in Malaysia and poses a significant threat to the local biodiversity?',
                'options': {
                    'A': "Malayan Tapir",
                    'B': "Asian Elephant",
                    'C': "Golden Apple Snail",
                    'D': "Sun Bear"
                },
                'correct_answer': 'Golden Apple Snail',
                'explanation': """The Golden Apple Snail is an invasive species in Malaysia, particularly affecting rice fields by damaging crops and disrupting local ecosystems. In contrast, the Malayan Tapir, Asian Elephant, and Sun Bear are native species crucial to Malaysia's biodiversity.""",
                'hint': "This species has a golden shell, and it feeds on young crops."
                },
                {
                'question': 'What is the primary reason why invasive species like the Common Myna thrive in Malaysia?',
                'options': {
                    'A': "They have natural predators in Malaysia",
                    'B': "They adapt easily to human-modified environments",
                    'C': "They cannot compete with native species",
                    'D': "They need very specific habitats"
                },
                'correct_answer': 'They adapt easily to human-modified environments',
                'explanation': """The Common Myna is an adaptable species that thrives in urban and rural areas in Malaysia, benefiting from human-modified environments such as cities and agricultural land. Their ability to exploit human resources helps them thrive and outcompete native species.""",
                'hint': "Think about how this species benefits from living in cities and other human-created environments."
                },
                {
                'question': 'How can the spread of invasive species in Malaysia be controlled?',
                'options': {
                    'A': "By promoting the growth of non-native species",
                    'B': "By introducing more invasive species",
                    'C': "By eradicating native species",
                    'D': "By preventing the introduction and spread of invasive species"
                },
                'correct_answer': 'By preventing the introduction and spread of invasive species',
                'explanation': """To control the spread of invasive species, measures include preventing the introduction of non-native species, controlling their populations in the wild, and protecting native species and habitats from further disruption. This can involve monitoring, regulation, education, and the removal of invasive species when necessary.""",
                'hint': "Prevention is always better than cure."
                }   
            ]
            
            # Add questions and relate them to the quiz
            for question_data in questions_data:
                quiz = Quiz(quiz_completed=False)  # Create a new quiz
                db.session.add(quiz)
                db.session.commit()  # Commit to get the quiz_id

                question = Question(
                    quiz_id=1,
                    question=question_data['question'],
                    option_a=question_data['options']['A'],
                    option_b=question_data['options']['B'],
                    option_c=question_data['options']['C'],
                    option_d=question_data['options']['D'],
                    correct_answer=question_data['correct_answer'],
                    explanation=question_data['explanation'],
                    hint=question_data['hint']
                )
                db.session.add(question)
                db.session.commit()

            return jsonify({"message": "All quiz questions added successfully!"}), 201


    @app.route("/") # Access at http://127.0.0.1:5000/
    def front_page(): # can be anything but should be descriptive
        return jsonify({"name":"superman"}), 200 
    # Returns {"name", "superman"} and response code of 200 (Use 200 for any successful request and 401 for unsucessful requests)

    # register route to /landing/
    from .landing_page import landing
    from .email import emailRoutes
    from .forgetPassword import forgetPassword
    app.register_blueprint(landing, url_prefix='/landing')
    app.register_blueprint(emailRoutes, url_prefix='/email')
    app.register_blueprint(forgetPassword, url_prefix='/forgetPassword')
   
    #register route to /user/
    from .user import user
    app.register_blueprint(user, url_prefix='/user')


    #method to retrieve all questions data
    @app.route('/quiz_all', methods=['GET']) # Access at http://127.0.0.1:5000/quiz_all
    def get_questions():
        try:
            questions = Question.query.all()  # Retrieve all questions
            question_data = []

            for question in questions:
                quiz = Quiz.query.get(question.quiz_id)
                quiz_completed = quiz.quiz_completed if quiz else False

                question_data.append({
                    "question_id": question.question_id,
                    "quiz_id": question.quiz_id,
                    "quiz_completed": quiz_completed,
                    "question": question.question,
                    "options": [question.option_a, question.option_b, question.option_c, question.option_d],
                    "answer": question.correct_answer,
                    "explanation": question.explanation,
                    "hint": question.hint,
                })

            return jsonify(question_data), 200
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    

    #method to retrieve completed quizzes
    @app.route('/quiz_all/completed', methods=['GET'])  # Access at http://127.0.0.1:5000/quiz_all/completed
    def get_completed_quizzes():

        try:
            quizzes = Quiz.query.filter_by(quiz_completed=True).all()
            data = []

            for quiz in quizzes:
                questions = Question.query.filter_by(quiz_id=quiz.quiz_id).all()
                question_data = []

                for question in questions:
                    question_data.append({
                        "question_id": question.question_id,
                        "question": question.question,
                        "options": [question.option_a, question.option_b, question.option_c, question.option_d],
                        "answer": question.correct_answer,
                        "explanation": question.explanation,
                        "hint": question.hint,
                    })

                data.append({
                    "quiz_id": quiz.quiz_id,
                    "quiz_completed": quiz.quiz_completed,
                    "questions": question_data,
                })

            return jsonify(data), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    

    # Method to get question hint for specific question
    @app.route('/questions/<int:question_id>/hint', methods=['GET']) # Access at http://127.0.0.1:5000/questions/<question_id>/hint
    def get_question_hint(question_id):
        try:
            # Query the database for the question
            question = Question.query.get(question_id)
            
            # If question doesn't exist, return 404
            if not question:
                return jsonify({"error": "Question not found"}), 404
            
            # Return the hint
            return jsonify({
                "question_id": question.question_id,
                "hint": question.hint
            }), 200

        except Exception as e:
            # Handle unexpected errors
            return jsonify({"error": str(e)}), 500
        
    # Method to bookmarking quiz id  
    @app.route('/bookmark', methods=['POST'])
    def bookmark_quiz():
        try:
            data = request.get_json()
            user_id = data.get('user_id')
            quiz_id = data.get('quiz_id')

            # Check if a bookmark already exists for the user
            bookmark = Bookmark.query.filter_by(user_id=user_id).first()
            if bookmark:
                # Update the existing bookmark
                bookmark.quiz_id = quiz_id
            else:
                # Create a new bookmark
                bookmark = Bookmark(user_id=user_id, quiz_id=quiz_id)
                db.session.add(bookmark)

            db.session.commit()
            return jsonify({"message": "Quiz "+quiz_id+" bookmarked successfully"}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
        
    # Method to get the bookmarked quiz id, null indicate no bookmarked quiz
    @app.route('/bookmark/<int:user_id>', methods=['GET'])
    def get_bookmark(user_id):
        try:
            # Get the bookmark for the user
            bookmark = Bookmark.query.filter_by(user_id=user_id).first()
            if bookmark and bookmark.quiz_id:
                return jsonify({"user_id": user_id, "quiz_id": bookmark.quiz_id}), 200
            else:
                return jsonify({"user_id": user_id, "message": "No quiz bookmarked"}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    # method to get completed TIME of a specific user by user ID
    @app.route('/user/<int:user_id>/completed', methods=['GET']) # Access at http://127.0.0.1:5000/user/<user_id>/completed
    def get_user_completed(user_id):
        try:
            user = User.query.get(user_id)
            if user is None:
                return jsonify({"error": f"User with ID {user_id} not found."}), 404
            
            if user.completed_at:
                return jsonify({
                    "user_id": user.user_id,
                    "username": user.username,
                    "completed_at": user.completed_at.isoformat()
                }), 200
            else:
                return jsonify({
                    "user_id": user.user_id,
                    "username": user.username,
                    "message": "User has not completed the quiz."
                }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    # method to get the quiz completed time of ALL users
    @app.route('/users/completed', methods=['GET']) # Access at http://127.0.0.1:5000/users/completed
    def get_all_completed_users():
        try:
            users = User.query.filter(User.completed_at.isnot(None)).all()
            user_data = [
                {
                    "user_id": user.user_id,
                    "username": user.username,
                    "completed_at": user.completed_at.isoformat()
                }
                for user in users
            ]
            return jsonify(user_data), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500         


    #method to get all users' score
    @app.route('/users/scores', methods=['GET']) #Access at http://127.0.0.1:5000/users/scores
    def get_all_user_scores():
        """Retrieve all users and their scores."""
        try:
            users = User.query.all()  # Fetch all users
            user_scores = [
                {"user_id": user.user_id, "username": user.username, "score": user.score}
                for user in users
            ]
            return jsonify({"data": user_scores}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500


    # method to register new user
    @app.route('/add_user', methods=['POST'])
    def add_user():
        try:
            data = request.get_json()  # Get JSON data from request
            new_user = User(
            username = data.get('username'),
            email = data.get('email'),
            password = data.get('password'),
            score = None
            )

            # Insert user into the SQLite database
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"message": "User added successfully"}), 201
        except Exception as e:
            db.session.rollback()  # Rollback in case of any exception
            return jsonify({"error": str(e)}), 500


    #method to get all user details
    @app.route('/users', methods=['GET'])
    def get_users():
        users = User.query.all()
        user_list = [{"id": user.user_id, "username": user.username, "email": user.email, "password": user.password, "score": user.score} for user in users]
        
        # Wrap the response in an array object for easier handling in frontend
        response = {
            "users": user_list  # Returning the user list inside a "users" array
        }
        
        return jsonify(user_list), 200


    #method to login users
    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Check if the user exists in the database
        user = User.query.filter_by(username=username).first()
    
        if user:
            # If user exists, check if the password matches (no hashing)
            if user.password == password:
                session['user_id'] = user.user_id  # Store user_id in session
                return jsonify({"message": "Login successful"}), 200
            else:
                return jsonify({"error": "Wrong password"}), 401
        else:
            # If user does not exist, redirect to the registration page
            return jsonify({"error": "Invalid password or username"}), 401


    #method to logout users
    @app.route('/logout', methods=['POST'])
    def logout():
        session.pop('user_id', None)  # Remove user_id from session
        return jsonify({"message": "Logged out successfully"}), 200


    # Create database object instance
    create_database(app)
    
    return app

def create_database(app : Flask):

    with app.app_context():

        db.create_all()
        print('Created Database!')
