from flask import Flask
from . import db

class Question(db.Model): # Question class is a child class of Model class
    # we need to tell Question what columns are present
    question_id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'), nullable=False)
    question = db.Column(db.Text, nullable= False)
    option_a = db.Column(db.Text, nullable=False)
    option_b = db.Column(db.Text, nullable=False)
    option_c = db.Column(db.Text, nullable=False)
    option_d = db.Column(db.Text, nullable=False)
    correct_answer = db.Column(db.Text, nullable=False)
    explanation = db.Column(db.Text)
    hint = db.Column(db.Text, nullable=False)

    quiz = db.relationship('Quiz', back_populates='questions')

    def __repr__(self): # what is shown when we print() object, Representation of a Question object 
        return f"<Question {self.question_id}, Quiz ID: {self.quiz_id}>"

class Quiz(db.Model): # Stores quiz id and quiz completed
    quiz_id = db.Column(db.Integer, primary_key=True)
    quiz_completed = db.Column(db.Boolean, default=False)

    questions = db.relationship('Question', back_populates='quiz', cascade="all, delete")

    def __repr__(self):
        return f"<Quiz {self.quiz_id}, Completed: {self.quiz_completed}>"

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    score = db.Column(db.Integer)

    def __repr__(self):
        return f"<User {self.username}, Score: {self.score}, Completed At: {self.completed_at}>"

class Forum(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    post_content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(100), db.ForeignKey('user.username'), nullable=False)  # Foreign key on username
    created_at = db.Column(db.DateTime,nullable=False)

    user = db.relationship('User', backref=db.backref('posts', lazy=True), foreign_keys=[username])

    def __repr__(self):
        return f"<Forum Post {self.post_id} - {self.post_content}>"

class Bookmark(db.Model):
    bookmark_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'))