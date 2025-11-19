from flask_wtf import FlaskForm # type: ignore
from wtforms import StringField, PasswordField, SubmitField, SelectField, FloatField, TextAreaField, BooleanField, DateField # type: ignore
from wtforms.validators import DataRequired # type: ignore


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    username = StringField('Username')
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[('admin', 'Admin')], validators=[DataRequired()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class MarkForm(FlaskForm):
    student_id = StringField('Student ID', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    exam = StringField('Exam', validators=[DataRequired()])
    score = FloatField('Score', validators=[DataRequired()])
    max_score = FloatField('Max Score', validators=[DataRequired()])
    submit = SubmitField('Upload Mark')


class AttendanceForm(FlaskForm):
    student_id = StringField('Student ID', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Present', 'Present'), ('Absent', 'Absent')], validators=[DataRequired()])
    submit = SubmitField('Upload Attendance')


class AssignmentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    due_date = DateField('Due Date')
    submitted = BooleanField('Submitted')
    max_score = FloatField('Max Score')
    submit = SubmitField('Upload Assignment')


class AdminAddStudentForm(FlaskForm):
    name = StringField('Student Name', validators=[DataRequired()])
    email = StringField('Student Email', validators=[DataRequired()])
    contact = StringField('Student Contact')
    parent_name = StringField('Parent Name', validators=[DataRequired()])
    parent_email = StringField('Parent Email', validators=[DataRequired()])
    parent_contact = StringField('Parent Contact')
    class_name = StringField('Class', validators=[DataRequired()])
    division = SelectField('Division', choices=[('Div1', 'CSE DIV 1'), ('Div2', 'CSE DIV 2')], validators=[DataRequired()])
    password = StringField('Password (e.g., name123)', validators=[DataRequired()])
    submit = SubmitField('Add Student')


class AdminAddTeacherForm(FlaskForm):
    name = StringField('Teacher Name', validators=[DataRequired()])
    email = StringField('Teacher Email', validators=[DataRequired()])
    contact = StringField('Teacher Contact')
    subject = StringField('Subject', validators=[DataRequired()])
    division = SelectField('Division', choices=[('Div1', 'CSE DIV 1'), ('Div2', 'CSE DIV 2')], validators=[DataRequired()])
    password = StringField('Password (e.g., name123)', validators=[DataRequired()])
    submit = SubmitField('Add Teacher')


class AdminAddParentForm(FlaskForm):
    name = StringField('Parent Name', validators=[DataRequired()])
    email = StringField('Parent Email', validators=[DataRequired()])
    contact = StringField('Parent Contact')
    student_id = StringField('Link to Student ID', validators=[DataRequired()])
    password = StringField('Password (e.g., name123)', validators=[DataRequired()])
    submit = SubmitField('Add Parent')
