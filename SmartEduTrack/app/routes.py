
from flask import render_template, request, redirect, url_for, flash, send_file, Blueprint # type: ignore
from flask_login import login_user, current_user, logout_user, login_required # type: ignore
from . import db
from .models import User, Student, Teacher, Parent, Mark, Attendance, Assignment
from .forms import RegisterForm, LoginForm, MarkForm, AttendanceForm, AssignmentForm, AdminAddStudentForm, AdminAddTeacherForm, AdminAddParentForm
from .utils import render_pdf_from_template
from io import BytesIO

bp = Blueprint('main', __name__)

@bp.route('/assignment/<int:assignment_id>/update', methods=['POST'])
@login_required
def update_assignment(assignment_id):
    if current_user.role != 'teacher':
        return redirect(url_for('main.index'))
    
    student_id = request.form.get('student_id')
    if not student_id:
        flash('No student selected for grading', 'danger')
        return redirect(url_for('main.dashboard_teacher'))

    
    assignment = Assignment.query.filter_by(id=assignment_id, student_id=int(student_id)).first()
    if assignment is None:
        flash('Assignment for selected student not found', 'danger')
        return redirect(url_for('main.dashboard_teacher'))

    
    teacher = current_user.teacher_profile
    st = Student.query.get(assignment.student_id)
    if teacher and st and st.division != (teacher.division or 'Div1'):
        flash('You are not authorized to grade this student', 'danger')
        return redirect(url_for('main.dashboard_teacher'))

    submitted = request.form.get('submitted') == 'True'
    score = request.form.get('score')
    assignment.submitted = submitted
    if score is not None and score != '':
        try:
            assignment.score = float(score)
        except ValueError:
            flash('Invalid score value', 'danger')
            return redirect(url_for('main.dashboard_teacher'))
    db.session.commit()
    flash('Assignment updated successfully', 'success')
    return redirect(url_for('main.dashboard_teacher'))

@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        
        if form.role.data != 'admin':
            flash('Only admin can self-register. Use admin to add other users.', 'danger')
            return redirect(url_for('main.register'))

        if User.query.filter_by(email=form.email.data).first():
            flash('Email already exists', 'danger')
            return redirect(url_for('main.register'))

        user = User(username=form.username.data or form.email.data.split('@')[0], email=form.email.data, password=form.password.data, role=form.role.data)
        db.session.add(user)
        db.session.commit()

    

        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data, password=form.password.data).first()
        if user:
            login_user(user)
            if user.role == 'student':
                return redirect(url_for('main.dashboard_student'))
            if user.role == 'teacher':
                return redirect(url_for('main.dashboard_teacher'))
            if user.role == 'parent':
                return redirect(url_for('main.dashboard_parent'))
            if user.role == 'admin':
                return redirect(url_for('main.dashboard_admin'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/dashboard/student')
@login_required
def dashboard_student():
    if current_user.role != 'student':
        return redirect(url_for('main.index'))
    student = current_user.student_profile
    marks = Mark.query.filter_by(student_id=student.id).all()
    attendance = Attendance.query.filter_by(student_id=student.id).all()
    
    
    assignments = Assignment.query.filter_by(student_id=student.id).all()

    marks_data = [{
        "subject": m.subject,
        "score": m.score,
        "max": m.max_score
    } for m in marks]
    attendance_data = [{
        "date": (a.date.isoformat() if hasattr(a.date, 'isoformat') else str(a.date)),
        "status": a.status
    } for a in attendance]

    return render_template(
        'dashboard_student.html',
        student=student,
        marks_data=marks_data,
        attendance_data=attendance_data,
        assignments=assignments
    )


@bp.route('/dashboard/teacher', methods=['GET', 'POST'])
@login_required
def dashboard_teacher():
    if current_user.role != 'teacher':
        return redirect(url_for('main.index'))
    mark_form = MarkForm()
    attendance_form = AttendanceForm()
    assignment_form = AssignmentForm()

   
    teacher = current_user.teacher_profile
    teacher_div = teacher.division if teacher else 'Div1'
    students_in_div = Student.query.filter_by(division=teacher_div).all()

    if mark_form.submit.data and mark_form.validate_on_submit():
        m = Mark(student_id=int(mark_form.student_id.data), subject=mark_form.subject.data, exam=mark_form.exam.data, score=mark_form.score.data, max_score=mark_form.max_score.data)
        db.session.add(m)
        db.session.commit()
        flash('Mark uploaded', 'success')
        return redirect(url_for('main.dashboard_teacher'))

    if attendance_form.submit.data and attendance_form.validate_on_submit():
        student_id = int(attendance_form.student_id.data)
        date_val = attendance_form.date.data
        
        existing = Attendance.query.filter_by(student_id=student_id, date=date_val).first()
        if existing:
            flash('Attendance for this student on this date already exists', 'warning')
        else:
            a = Attendance(student_id=student_id, date=date_val, status=attendance_form.status.data)
            db.session.add(a)
            db.session.commit()
            flash('Attendance uploaded', 'success')
        return redirect(url_for('main.dashboard_teacher'))

    if assignment_form.submit.data and assignment_form.validate_on_submit():
      
        for st in students_in_div:
            asg = Assignment(
                student_id=st.id,
                title=assignment_form.title.data,
                description=assignment_form.description.data,
                due_date=assignment_form.due_date.data,
                submitted=assignment_form.submitted.data,
                max_score=assignment_form.max_score.data
            )
            db.session.add(asg)
        db.session.commit()
        flash('Assignment uploaded to all students in your class/division', 'success')
        return redirect(url_for('main.dashboard_teacher'))

  
    subjects = {}
    for m in Mark.query.all():
        subjects.setdefault(m.subject, []).append(m.score / (m.max_score or 100) * 100)
    avg_by_subject = {s: (sum(v)/len(v)) if v else 0 for s, v in subjects.items()}

  
    from collections import Counter
    attendance_records = Attendance.query.join(Student).filter(Student.division == teacher_div).all()
    attendance_by_date = {}
    for a in attendance_records:
        d = a.date.isoformat() if hasattr(a.date, 'isoformat') else str(a.date)
        attendance_by_date.setdefault(d, []).append(a.status)
    attendance_chart = {d: dict(Counter(v)) for d, v in attendance_by_date.items()}

   
    student_to_scores = {}
    for m in Mark.query.all():
        pct = (m.score / (m.max_score or 100)) * 100
        student_to_scores.setdefault(m.student_id, []).append(pct)
    weak_students = []
    for sid, pcts in student_to_scores.items():
        avg = sum(pcts) / len(pcts) if pcts else 100
        if avg < 40:
            st = Student.query.get(sid)
            weak_students.append({"id": st.id, "name": st.name, "avg": round(avg, 2)})

   
    assignments = Assignment.query.join(Student).filter(Student.division == teacher_div).all()

    return render_template(
        'dashboard_teacher.html',
        mark_form=mark_form,
        attendance_form=attendance_form,
        assignment_form=assignment_form,
        avg_by_subject=avg_by_subject,
        weak_students=weak_students,
        students_in_div=students_in_div,
        attendance_chart=attendance_chart,
        assignments=assignments
    )


@bp.route('/dashboard/parent')
@login_required
def dashboard_parent():
    if current_user.role != 'parent':
        return redirect(url_for('main.index'))
    parent = current_user.parent_profile
    student = parent.student
    marks = Mark.query.filter_by(student_id=student.id).all()
    attendance = Attendance.query.filter_by(student_id=student.id).all()

    marks_data = [{
        "subject": m.subject,
        "score": m.score,
        "max": m.max_score
    } for m in marks]
    attendance_data = [{
        "date": (a.date.isoformat() if hasattr(a.date, 'isoformat') else str(a.date)),
        "status": a.status
    } for a in attendance]

  
    from .models import Feedback
    feedbacks = Feedback.query.filter_by(student_id=student.id).order_by(Feedback.created_at.desc()).all()

    return render_template(
        'dashboard_parent.html',
        parent=parent,
        student=student,
        marks_data=marks_data,
        attendance_data=attendance_data,
        feedbacks=feedbacks
    )


@bp.route('/dashboard/admin')
@login_required
def dashboard_admin():
    if current_user.role != 'admin':
        return redirect(url_for('main.index'))
    students = Student.query.order_by(Student.class_name, Student.division, Student.roll_no).all()
    teachers = Teacher.query.order_by(Teacher.name).all()
    parents = Parent.query.order_by(Parent.name).all()
    return render_template('dashboard_admin.html', users=User.query.all(), students=students, teachers=teachers, parents=parents, add_student_form=AdminAddStudentForm(), add_teacher_form=AdminAddTeacherForm(), add_parent_form=AdminAddParentForm())


@bp.route('/admin/add-student', methods=['POST'])
@login_required
def admin_add_student():
    if current_user.role != 'admin':
        return redirect(url_for('main.index'))
    form = AdminAddStudentForm()
    if form.validate_on_submit():
     
        if User.query.filter_by(email=form.email.data).first():
            flash('Student email already exists', 'danger')
            return redirect(url_for('main.dashboard_admin'))
        user = User(username=form.name.data, email=form.email.data, password=form.password.data, role='student')
        db.session.add(user)
        db.session.flush()
    
        existing = Student.query.filter_by(class_name=form.class_name.data, division=form.division.data).count()
        roll_no = existing + 1
        st = Student(user_id=user.id, name=form.name.data, email=form.email.data, contact=form.contact.data, parent_name=form.parent_name.data, parent_email=form.parent_email.data, parent_contact=form.parent_contact.data, class_name=form.class_name.data, division=form.division.data, roll_no=roll_no)
        db.session.add(st)
        db.session.commit()
        flash('Student added', 'success')
    return redirect(url_for('main.dashboard_admin'))


@bp.route('/admin/add-teacher', methods=['POST'])
@login_required
def admin_add_teacher():
    if current_user.role != 'admin':
        return redirect(url_for('main.index'))
    form = AdminAddTeacherForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Teacher email already exists', 'danger')
            return redirect(url_for('main.dashboard_admin'))
        user = User(username=form.name.data, email=form.email.data, password=form.password.data, role='teacher')
        db.session.add(user)
        db.session.flush()
        t = Teacher(user_id=user.id, name=form.name.data, email=form.email.data, contact=form.contact.data, subject=form.subject.data, division=form.division.data)
        db.session.add(t)
        db.session.commit()
        flash('Teacher added', 'success')
    return redirect(url_for('main.dashboard_admin'))


@bp.route('/admin/add-parent', methods=['POST'])
@login_required
def admin_add_parent():
    if current_user.role != 'admin':
        return redirect(url_for('main.index'))
    form = AdminAddParentForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Parent email already exists', 'danger')
            return redirect(url_for('main.dashboard_admin'))
        user = User(username=form.name.data, email=form.email.data, password=form.password.data, role='parent')
        db.session.add(user)
        db.session.flush()
        st = Student.query.get(int(form.student_id.data))
        if st is None:
            flash('Student not found', 'danger')
            return redirect(url_for('main.dashboard_admin'))
        p = Parent(user_id=user.id, name=form.name.data, email=form.email.data, contact=form.contact.data, student_id=st.id)
        db.session.add(p)
        db.session.commit()
        flash('Parent added', 'success')
    return redirect(url_for('main.dashboard_admin'))


@bp.route('/progress-card/<int:student_id>')
@login_required
def progress_card(student_id):
    student = Student.query.get_or_404(student_id)
    marks = Mark.query.filter_by(student_id=student.id).all()
    attendance = Attendance.query.filter_by(student_id=student.id).all()
    assignments = Assignment.query.filter_by(student_id=student.id).all()
    return render_template('progress_card.html', student=student, marks=marks, attendance=attendance, assignments=assignments)


@bp.route('/progress-card/<int:student_id>/pdf')
@login_required
def progress_card_pdf(student_id):
    student = Student.query.get_or_404(student_id)
    marks = Mark.query.filter_by(student_id=student.id).all()
    attendance = Attendance.query.filter_by(student_id=student.id).all()
    assignments = Assignment.query.filter_by(student_id=student.id).all()
    pdf_bytes = render_pdf_from_template('progress_card.html', student=student, marks=marks, attendance=attendance, assignments=assignments)
    return send_file(BytesIO(pdf_bytes), mimetype='application/pdf', as_attachment=True, download_name=f"progress_card_{student.id}.pdf")


@bp.route('/seed')
def seed():

    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', password='admin', role='admin')
        db.session.add(admin)
   
    for i in range(1, 6):
        uname = f"student{i}"
        user = User.query.filter_by(username=uname).first()
        if not user:
            user = User(username=uname, password='pass', role='student')
            db.session.add(user)
            db.session.flush()
            st = Student(user_id=user.id, name=f"Student {i}", class_name='Class A')
            db.session.add(st)
            db.session.flush()
          
            for subj, scores in {'Math':[20+i*5, 30+i*5], 'Science':[25+i*4, 35+i*4]}.items():
                for idx, sc in enumerate(scores):
                    db.session.add(Mark(student_id=st.id, subject=subj, exam=f"Test {idx+1}", score=sc, max_score=100))
           
            for d in range(1, 11):
                status = 'Present' if (d + i) % 5 != 0 else 'Absent'
                db.session.add(Attendance(student_id=st.id, status=status))
  
    if not User.query.filter_by(username='teacher1').first():
        tuser = User(username='teacher1', password='pass', role='teacher')
        db.session.add(tuser)
        db.session.flush()
        db.session.add(Teacher(user_id=tuser.id, name='Teacher One', subject='Math'))
 
    if not User.query.filter_by(username='parent1').first():
        puser = User(username='parent1', password='pass', role='parent')
        db.session.add(puser)
        db.session.flush()
        st1 = Student.query.first()
        if st1:
            db.session.add(Parent(user_id=puser.id, name='Parent One', student_id=st1.id))
    db.session.commit()
    flash('Seeded demo users and data', 'success')
    return redirect(url_for('main.index'))


