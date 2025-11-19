from datetime import datetime
from . import db, login_manager
from flask_login import UserMixin # type: ignore


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))  
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  
    role = db.Column(db.String(20), nullable=False)  

    student_profile = db.relationship("Student", backref="user", uselist=False)
    teacher_profile = db.relationship("Teacher", backref="user", uselist=False)
    parent_profile = db.relationship("Parent", backref="user", uselist=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True)
    contact = db.Column(db.String(30))
    parent_name = db.Column(db.String(120))
    parent_email = db.Column(db.String(120))
    parent_contact = db.Column(db.String(30))
    class_name = db.Column(db.String(50), nullable=False)  
    division = db.Column(db.String(20), nullable=False, default='Div1')  
    roll_no = db.Column(db.Integer)

    marks = db.relationship("Mark", backref="student", lazy=True, cascade="all, delete-orphan")
    attendance = db.relationship("Attendance", backref="student", lazy=True, cascade="all, delete-orphan")
    assignments = db.relationship("Assignment", backref="student", lazy=True, cascade="all, delete-orphan")


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True)
    contact = db.Column(db.String(30))
    subject = db.Column(db.String(120), nullable=False)
    division = db.Column(db.String(20), nullable=False, default='Div1')


class Parent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True)
    contact = db.Column(db.String(30))
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    student = db.relationship("Student", backref="parents")


class Mark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    subject = db.Column(db.String(120), nullable=False)
    exam = db.Column(db.String(120), nullable=False)
    score = db.Column(db.Float, nullable=False)
    max_score = db.Column(db.Float, nullable=False, default=100)
    date = db.Column(db.Date, default=datetime.utcnow)


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)
    status = db.Column(db.String(10), nullable=False)  


class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    submitted = db.Column(db.Boolean, default=False)
    score = db.Column(db.Float)
    max_score = db.Column(db.Float, default=100.0)
    due_date = db.Column(db.Date)


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teacher.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    note = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.Date, default=datetime.utcnow)



