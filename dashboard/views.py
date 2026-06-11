import json
import random
from datetime import datetime, date
from functools import wraps
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.db.models import Q
from .models import (
    Student, Teacher, Course, ActivityLog, UserProfile,
    Batch, StudentProfile, LearningMaterial, MCQ, MCQAttempt,
    CodingChallenge, CodingChallengeSubmission, Assignment,
    AssignmentSubmission, Announcement, StudentProgress, WeeklyScheduleOverride,
    ClassSchedule
)


# ==========================================
# Database Seeder Helper
# ==========================================
def seed_default_data():
    # Only seed if no records exist in Student, Teacher, or Course
    if not Student.objects.exists():
        default_students = [
            { 'student_id': '101', 'name': 'Srikanth', 'email': 'srikanth@gmail.com', 'course': 'Python Full Stack', 'status': 'Active' },
            { 'student_id': '102', 'name': 'Rahul', 'email': 'rahul@gmail.com', 'course': 'Java', 'status': 'Inactive' },
            { 'student_id': '103', 'name': 'Anjali', 'email': 'anjali@gmail.com', 'course': 'Web Development', 'status': 'Active' },
            { 'student_id': '104', 'name': 'praveen', 'email': 'srikanth2@gmail.com', 'course': 'Python Full Stack', 'status': 'Active' },
            { 'student_id': '105', 'name': 'Sravani', 'email': 'sravani@gmail.com', 'course': 'Python Full Stack', 'status': 'Active' },
            { 'student_id': '106', 'name': 'premm', 'email': 'prem@gmail.com', 'course': 'React', 'status': 'Active' },
            { 'student_id': '107', 'name': 'sai', 'email': 'sai@gmail.com', 'course': 'Python Full Stack', 'status': 'Active' },
            { 'student_id': '108', 'name': 'ganesh', 'email': 'ganesh@gmail.com', 'course': 'flutter', 'status': 'Active' },
            { 'student_id': '109', 'name': 'mahesh', 'email': 'mahesh@gmail.com', 'course': 'Java', 'status': 'Active' },
            { 'student_id': '110', 'name': 'vinay', 'email': 'vinay@gmail.com', 'course': 'Java', 'status': 'Active' }
        ]
        for s in default_students:
            Student.objects.create(**s)

    if not Teacher.objects.exists():
        default_teachers = [
            { 'teacher_id': '201', 'name': 'Vijay Kumar', 'email': 'vijay@gmail.com', 'spec': 'Python Full Stack', 'exp': '8 Years', 'status': 'Active' },
            { 'teacher_id': '202', 'name': 'Prasad Roy', 'email': 'prasad@gmail.com', 'spec': 'Java Development', 'exp': '10 Years', 'status': 'Active' },
            { 'teacher_id': '203', 'name': 'Sneha Reddy', 'email': 'sneha@gmail.com', 'spec': 'Web Development', 'exp': '5 Years', 'status': 'Active' },
            { 'teacher_id': '204', 'name': 'Suresh Kumar', 'email': 'suresh@gmail.com', 'spec': 'React JS', 'exp': '6 Years', 'status': 'Active' },
            { 'teacher_id': '205', 'name': 'Naveen Kumar', 'email': 'naveen@gmail.com', 'spec': 'Flutter Mobile App', 'exp': '4 Years', 'status': 'Active' }
        ]
        for t in default_teachers:
            Teacher.objects.create(**t)

    if not Course.objects.exists():
        default_courses = [
            { 'course_id': '1001', 'title': 'Python Full Stack', 'teacher': 'Vijay Kumar', 'category': 'Programming', 'duration': '6 Months', 'status': 'Active' },
            { 'course_id': '1002', 'title': 'Java Development', 'teacher': 'Prasad Roy', 'category': 'Programming', 'duration': '4 Months', 'status': 'Active' },
            { 'course_id': '1003', 'title': 'Web Development', 'teacher': 'Sneha Reddy', 'category': 'Design', 'duration': '3 Months', 'status': 'Active' },
            { 'course_id': '1004', 'title': 'React JS', 'teacher': 'Suresh Kumar', 'category': 'Development', 'duration': '2 Months', 'status': 'Active' },
            { 'course_id': '1005', 'title': 'Flutter Mobile App', 'teacher': 'Naveen Kumar', 'category': 'Mobile', 'duration': '3 Months', 'status': 'Active' }
        ]
        for c in default_courses:
            Course.objects.create(**c)

    if not ActivityLog.objects.exists():
        ActivityLog.objects.create(
            action="System Started",
            details="Dashboard initialized. Ready to accept student records."
        )

    # Seed Batches
    if not Batch.objects.exists() and Course.objects.exists():
        py_course = Course.objects.filter(title='Python Full Stack').first()
        if py_course:
            Batch.objects.create(name="Python Full Stack - Batch A", course=py_course)
        java_course = Course.objects.filter(title='Java Development').first()
        if java_course:
            Batch.objects.create(name="Java Development - Batch A", course=java_course)

    # Associate default students with batches & set password/details
    py_batch = Batch.objects.filter(name="Python Full Stack - Batch A").first()
    java_batch = Batch.objects.filter(name="Java Development - Batch A").first()
    
    for student in Student.objects.all():
        try:
            # Sync user creation first if not done by signal
            username = student.email
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, email=student.email, password=student.student_id)
                user.first_name = student.name
                user.save()
            else:
                user = User.objects.get(username=username)

            profile, created = StudentProfile.objects.get_or_create(
                user=user,
                student_obj=student,
                defaults={
                    'full_name': student.name,
                    'student_id': student.student_id,
                    'email': student.email,
                    'course_name': student.course,
                }
            )
            
            if not profile.batch:
                if "python" in student.course.lower() and py_batch:
                    profile.batch = py_batch
                elif "java" in student.course.lower() and java_batch:
                    profile.batch = java_batch
                profile.joining_date = "2026-01-15"
                profile.mobile_number = "9876543210"
                profile.address = "123 Academic Street, Hyderabad, India"
                profile.date_of_birth = "2000-05-15"
                profile.gender = "Male"
                profile.educational_qualification = "B.Tech Computer Science"
                profile.previous_study_details = "Intermediate (MPC)"
                profile.college_university_name = "JNTU Hyderabad"
                profile.emergency_contact = "9876543211"
                profile.save()
        except Exception as e:
            pass

    # Seed Learning Materials
    if not LearningMaterial.objects.exists():
        materials = [
            {
                'title': 'Python Full Stack Notes - Complete Basics',
                'material_type': 'technical_notes',
                'file_type': 'PDF',
                'file_url': 'python_basics.pdf',
                'content': 'Welcome to Python Full Stack. This notes document covers python syntax, lists, tuples, dictionaries, conditionals, loops, functions, and basics of Object Oriented Programming in Python.',
                'course_name': 'Python Full Stack'
            },
            {
                'title': 'Introduction to Django Framework MVT architecture',
                'material_type': 'technical_notes',
                'file_type': 'Video',
                'file_url': 'django_intro.mp4',
                'content': 'A comprehensive introductory guide to Django. It explains Model-View-Template architecture, directory structures, settings file, and configuring simple routing patterns.',
                'course_name': 'Python Full Stack'
            },
            {
                'title': 'Aptitude Preparation - Quantitative Skills',
                'material_type': 'aptitude',
                'file_type': 'PDF',
                'file_url': 'quantitative_aptitude.pdf',
                'content': 'Standard practice questions and formulas on profit & loss, time and work, speed-distance-time, average, percentage, and ratio-proportion calculations.',
                'course_name': 'Python Full Stack'
            },
            {
                'title': 'English Communication - Mock Interview Grooming',
                'material_type': 'english',
                'file_type': 'Document',
                'file_url': 'resume_template.docx',
                'content': 'Professional tips on greeting panels, formatting resume sections, outlining technical qualifications, highlighting portfolio projects, and structured body language advice.',
                'course_name': 'Python Full Stack'
            },
            {
                'title': 'Python Full Stack Interview FAQ',
                'material_type': 'interview_q',
                'file_type': 'Link',
                'file_url': 'https://example.com/interview-qa',
                'content': 'Comprehensive cheat sheet containing 50 frequently asked questions covering list comprehensions, decorators, multi-threading, REST API methods, database joins, and index optimizations.',
                'course_name': 'Python Full Stack'
            },
            {
                'title': 'Java Development Core Concepts',
                'material_type': 'technical_notes',
                'file_type': 'PDF',
                'file_url': 'java_basics.pdf',
                'content': 'Java Virtual Machine architecture, memory footprint, static variables vs instance variables, garbage collection algorithms, streams, and threading models.',
                'course_name': 'Java Development'
            }
        ]
        for m in materials:
            LearningMaterial.objects.create(**m)

    # Seed MCQs
    if not MCQ.objects.exists():
        mcqs = [
            {
                'category': 'Python',
                'question_text': 'Which of the following is an immutable data structure in Python?',
                'option_a': 'List',
                'option_b': 'Dictionary',
                'option_c': 'Tuple',
                'option_d': 'Set',
                'correct_option': 'C'
            },
            {
                'category': 'Python',
                'question_text': 'What is the output of print(2 ** 3) in Python?',
                'option_a': '6',
                'option_b': '8',
                'option_c': '9',
                'option_d': '16',
                'correct_option': 'B'
            },
            {
                'category': 'HTML',
                'question_text': 'Which tag is used to create a hyperlink in HTML?',
                'option_a': '<link>',
                'option_b': '<a>',
                'option_c': '<href>',
                'option_d': '<src>',
                'correct_option': 'B'
            },
            {
                'category': 'CSS',
                'question_text': 'Which property is used to change the background color in CSS?',
                'option_a': 'color',
                'option_b': 'background-color',
                'option_c': 'bgcolor',
                'option_d': 'color-bg',
                'correct_option': 'B'
            },
            {
                'category': 'SQL',
                'question_text': 'Which SQL keyword is used to retrieve data from a database?',
                'option_a': 'GET',
                'option_b': 'SELECT',
                'option_c': 'EXTRACT',
                'option_d': 'FETCH',
                'correct_option': 'B'
            },
            {
                'category': 'Aptitude',
                'question_text': 'A train running at the speed of 60 km/hr crosses a pole in 9 seconds. What is the length of the train?',
                'option_a': '120 meters',
                'option_b': '150 meters',
                'option_c': '180 meters',
                'option_d': '200 meters',
                'correct_option': 'B'
            }
        ]
        for q in mcqs:
            MCQ.objects.create(**q)

    # Seed Coding Challenges
    if not CodingChallenge.objects.exists():
        challenges = [
            {
                'title': 'Reverse a String',
                'difficulty': 'Easy',
                'description': 'Write a function that takes a string input and returns its reverse.',
                'input_format': 'A single line containing a string.',
                'output_format': 'A single line containing the reversed string.',
                'sample_input': 'hello',
                'sample_output': 'olleh',
                'sample_solution': 'def reverse_string(s):\n    return s[::-1]',
                'category': 'Python'
            },
            {
                'title': 'Check Prime Number',
                'difficulty': 'Medium',
                'description': 'Write a program to verify if a given integer n is prime.',
                'input_format': 'An integer n.',
                'output_format': 'True if n is prime, False otherwise.',
                'sample_input': '11',
                'sample_output': 'True',
                'sample_solution': 'def is_prime(n):\n    if n <= 1: return False\n    for i in range(2, int(n**0.5) + 1):\n        if n % i == 0: return False\n    return True',
                'category': 'Python'
            },
            {
                'title': 'Fibonacci Sequence Generator',
                'difficulty': 'Hard',
                'description': 'Generate the first n Fibonacci numbers as a list.',
                'input_format': 'An integer n.',
                'output_format': 'A list containing n integers.',
                'sample_input': '5',
                'sample_output': '[0, 1, 1, 2, 3]',
                'sample_solution': 'def fibonacci(n):\n    if n <= 0: return []\n    if n == 1: return [0]\n    seq = [0, 1]\n    while len(seq) < n:\n        seq.append(seq[-1] + seq[-2])\n    return seq',
                'category': 'Python'
            }
        ]
        for c in challenges:
            CodingChallenge.objects.create(**c)

    # Seed Assignments
    if not Assignment.objects.exists():
        assignments = [
            {
                'title': 'Django Blog Application',
                'description': 'Create a basic blog application with views for listing posts, detailed post display, and adding comments.',
                'course_name': 'Python Full Stack',
                'due_date': '2026-06-25'
            },
            {
                'title': 'HTML and CSS Landing Page',
                'description': 'Design a responsive landing page for a startup using pure HTML and CSS flexbox.',
                'course_name': 'Python Full Stack',
                'due_date': '2026-06-18'
            }
        ]
        for a in assignments:
            Assignment.objects.create(**a)

    # Seed Announcements
    if not Announcement.objects.exists():
        announcements = [
            {
                'title': 'Python Full Stack Guest Lecture',
                'content': 'We have a guest lecture by a Senior Architect on Microservices integration this Friday at 10:00 AM. Attendance is mandatory.',
                'course_name': 'Python Full Stack'
            },
            {
                'title': 'Mock Interviews Schedule',
                'content': 'Technical mock interviews for all final term students will commence from next Monday. Please prepare core subjects.',
                'course_name': 'All'
            }
        ]
        for ann in announcements:
            Announcement.objects.create(**ann)


# ==========================================
# Role-based Access Control Decorators
# ==========================================
def admin_page_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if hasattr(request.user, 'student_profile'):
            return redirect('student_dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def admin_api_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or hasattr(request.user, 'student_profile'):
            return JsonResponse({'error': 'Unauthorized: Access denied'}, status=403)
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# ==========================================
# Page Views
# ==========================================
@ensure_csrf_cookie
def login_view(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'student_profile'):
            return redirect('student_dashboard')
        return redirect('index')
    return render(request, 'login.html')

@ensure_csrf_cookie
def register_view(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'student_profile'):
            return redirect('student_dashboard')
        return redirect('index')
    return render(request, 'register.html')

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return render(request, 'logout.html')

@admin_page_required
@ensure_csrf_cookie
def index_view(request):
    seed_default_data()
    return render(request, 'index.html')

@admin_page_required
@ensure_csrf_cookie
def student_view(request):
    return render(request, 'student.html')

@admin_page_required
@ensure_csrf_cookie
def courses_view(request):
    return render(request, 'courses.html')

@admin_page_required
@ensure_csrf_cookie
def teachers_view(request):
    return render(request, 'teachers.html')

@admin_page_required
def schedule_view(request):
    return redirect('index')

@admin_page_required
def reports_view(request):
    return redirect('index')

@admin_page_required
@ensure_csrf_cookie
def settings_view(request):
    return render(request, 'settings.html')


@admin_page_required
@ensure_csrf_cookie
def manage_lms_view(request):
    batches = Batch.objects.all()
    courses = Course.objects.all()
    return render(request, 'manage_lms.html', {'batches': batches, 'courses': courses})


@admin_page_required
@ensure_csrf_cookie
def manage_mcq_view(request):
    return render(request, 'manage_mcq.html')


@admin_page_required
@ensure_csrf_cookie
def manage_coding_view(request):
    return render(request, 'manage_coding.html')


@admin_page_required
@ensure_csrf_cookie
def manage_schedule_view(request):
    batches = Batch.objects.all()
    courses = Course.objects.all()
    return render(request, 'manage_schedule.html', {'batches': batches, 'courses': courses})


@admin_page_required
@ensure_csrf_cookie
def manage_assignments_view(request):
    batches = Batch.objects.all()
    courses = Course.objects.all()
    return render(request, 'manage_assignments.html', {'batches': batches, 'courses': courses})




# ==========================================
# Auth API Views
# ==========================================
@require_http_methods(["POST"])
def api_login(request):
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        password = data.get('password', '')
        role = data.get('role', 'admin').strip()

        if not email or not password:
            return JsonResponse({'error': 'Email and Password are required'}, status=400)

        # Authenticate using username (find matching user by email + role or username + role)
        username = email
        user_obj = None
        try:
            if role == 'student':
                user_obj = User.objects.filter(email=email, student_profile__isnull=False).first()
                if not user_obj:
                    user_obj = User.objects.filter(username=email, student_profile__isnull=False).first()
            else:  # admin
                user_obj = User.objects.filter(email=email, student_profile__isnull=True).first()
                if not user_obj:
                    user_obj = User.objects.filter(username=email, student_profile__isnull=True).first()
            
            if user_obj:
                username = user_obj.username
        except Exception:
            pass

        user = authenticate(request, username=username, password=password)
        if user is not None:
            is_student_user = hasattr(user, 'student_profile')
            
            if role == 'student' and not is_student_user:
                return JsonResponse({'error': 'Unauthorized: Not a student account'}, status=403)
            elif role == 'admin' and is_student_user:
                return JsonResponse({'error': 'Unauthorized: Student accounts cannot access the admin portal'}, status=403)

            login(request, user)
            
            # Log this activity
            if is_student_user:
                ActivityLog.objects.create(
                    action="Student Logged In",
                    details=f"Student {user.username} authenticated successfully."
                )
                return JsonResponse({
                    'message': 'Logged in successfully',
                    'redirect': '/student/dashboard.html'
                })
            else:
                ActivityLog.objects.create(
                    action="Admin Logged In",
                    details=f"User {user.username} authenticated successfully."
                )
                return JsonResponse({
                    'message': 'Logged in successfully',
                    'redirect': '/index.html'
                })
        else:
            # Check if they exist with correct password under the other role to give a specific error
            other_user_obj = None
            try:
                if role == 'admin':
                    other_user_obj = User.objects.filter(email=email, student_profile__isnull=False).first()
                    if not other_user_obj:
                        other_user_obj = User.objects.filter(username=email, student_profile__isnull=False).first()
                else:
                    other_user_obj = User.objects.filter(email=email, student_profile__isnull=True).first()
                    if not other_user_obj:
                        other_user_obj = User.objects.filter(username=email, student_profile__isnull=True).first()
                
                if other_user_obj:
                    other_user = authenticate(request, username=other_user_obj.username, password=password)
                    if other_user is not None:
                        if role == 'admin':
                            return JsonResponse({'error': 'Unauthorized: Student accounts cannot access the admin portal'}, status=403)
                        else:
                            return JsonResponse({'error': 'Unauthorized: Not a student account'}, status=403)
            except Exception:
                pass
            
            return JsonResponse({'error': 'Invalid email or password'}, status=401)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
def api_register(request):
    try:
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')

        if not name or not email or not password:
            return JsonResponse({'error': 'All fields are required'}, status=400)

        # Enforce email uniqueness check across all users, students, and student profiles
        if User.objects.filter(email=email).exists() or Student.objects.filter(email=email).exists() or StudentProfile.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already registered'}, status=400)

        # Create unique username from email
        username = email.split('@')[0]
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = name
        user.save()

        # Create UserProfile
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.admin_name = name
        profile.admin_email = email
        profile.save()

        login(request, user)

        # Log action
        ActivityLog.objects.create(
            action="Admin Registered",
            details=f"New admin user registered: {name} ({email})"
        )

        return JsonResponse({'message': 'Registered and logged in successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@ensure_csrf_cookie
def student_register_view(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'student_profile'):
            return redirect('student_dashboard')
        return redirect('index')
    return render(request, 'student_register.html')


@require_http_methods(["POST"])
def api_student_register(request):
    try:
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        course = data.get('course', '').strip()

        if not name or not email or not password or not course:
            return JsonResponse({'error': 'All fields are required'}, status=400)

        # Enforce email uniqueness check across all users, students, and student profiles
        if User.objects.filter(email=email).exists() or Student.objects.filter(email=email).exists() or StudentProfile.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already registered'}, status=400)

        # Create unique username from email
        username = email.split('@')[0]
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = name
        user.save()

        # Generate student_id
        existing = Student.objects.all()
        if existing.exists():
            try:
                max_id = max(int(s.student_id) for s in existing if s.student_id.isdigit())
                new_id = str(max_id + 1)
            except Exception:
                new_id = str(Student.objects.count() + 101)
        else:
            new_id = '101'

        student = Student.objects.create(
            student_id=new_id,
            name=name,
            email=email,
            course=course,
            status='Active'
        )
        
        # Associate default batch if exists
        try:
            profile = StudentProfile.objects.get(student_obj=student)
            py_batch = Batch.objects.filter(name="Python Full Stack - Batch A").first()
            java_batch = Batch.objects.filter(name="Java Development - Batch A").first()
            if "python" in course.lower() and py_batch:
                profile.batch = py_batch
            elif "java" in course.lower() and java_batch:
                profile.batch = java_batch
            profile.save()
        except StudentProfile.DoesNotExist:
            pass

        login(request, user)

        ActivityLog.objects.create(
            action="Student Registered",
            details=f"New student registered: {name} (Course: {course})"
        )

        return JsonResponse({
            'message': 'Registered and logged in successfully',
            'redirect': '/student/dashboard.html'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)




# ==========================================
# Student API Views
# ==========================================
@admin_api_required
@require_http_methods(["GET", "POST"])
def api_students(request):
    if request.method == "GET":
        students = Student.objects.all().order_by('id')
        student_list = list(students.values('id', 'student_id', 'name', 'email', 'course', 'status'))
        return JsonResponse({'students': student_list})

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get('name', '').strip()
            email = data.get('email', '').strip()
            course = data.get('course', '').strip()
            status = data.get('status', 'Active')

            if not name or not email or not course:
                return JsonResponse({'error': 'Name, email and course are required'}, status=400)

            # Enforce unique email check
            if User.objects.filter(email=email).exists() or Student.objects.filter(email=email).exists() or StudentProfile.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already registered'}, status=400)

            # Generate student_id
            existing = Student.objects.all()
            if existing.exists():
                try:
                    max_id = max(int(s.student_id) for s in existing if s.student_id.isdigit())
                    new_id = str(max_id + 1)
                except Exception:
                    new_id = str(Student.objects.count() + 101)
            else:
                new_id = '101'

            student = Student.objects.create(
                student_id=new_id,
                name=name,
                email=email,
                course=course,
                status=status
            )

            # Log activity
            ActivityLog.objects.create(
                action="Student Enrolled",
                details=f"Enrolled new student: {name} (Course: {course})"
            )

            return JsonResponse({'id': student.id, 'student_id': student.student_id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@admin_api_required
@require_http_methods(["GET", "PUT", "DELETE"])
def api_student_detail(request, pk):
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)

    if request.method == "GET":
        return JsonResponse({
            'id': student.id,
            'student_id': student.student_id,
            'name': student.name,
            'email': student.email,
            'course': student.course,
            'status': student.status
        })

    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            new_email = data.get('email', student.email).strip()
            if new_email != student.email:
                if User.objects.filter(email=new_email).exists() or Student.objects.filter(email=new_email).exclude(pk=student.pk).exists() or StudentProfile.objects.filter(email=new_email).exists():
                    return JsonResponse({'error': 'Email already registered by another account'}, status=400)
                student.email = new_email

            student.name = data.get('name', student.name).strip()
            student.course = data.get('course', student.course).strip()
            student.status = data.get('status', student.status)
            student.save()

            # Log activity
            ActivityLog.objects.create(
                action="Student Updated",
                details=f"Updated details for student: {student.name}"
            )

            return JsonResponse({'message': 'Student updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == "DELETE":
        name = student.name
        student.delete()

        # Log activity
        ActivityLog.objects.create(
            action="Student Removed",
            details=f"Deleted profile of student: {name}"
        )

        return JsonResponse({'message': 'Student deleted successfully'})


# ==========================================
# Teacher API Views
# ==========================================
@admin_api_required
@require_http_methods(["GET", "POST"])
def api_teachers(request):
    if request.method == "GET":
        teachers = Teacher.objects.all().order_by('id')
        teacher_list = list(teachers.values('id', 'teacher_id', 'name', 'email', 'spec', 'exp', 'status'))
        return JsonResponse({'teachers': teacher_list})

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get('name', '').strip()
            email = data.get('email', '').strip()
            spec = data.get('spec', '').strip()
            exp = data.get('exp', '').strip()
            status = data.get('status', 'Active')

            if not name or not email or not spec or not exp:
                return JsonResponse({'error': 'All fields are required'}, status=400)

            # Generate teacher_id
            existing = Teacher.objects.all()
            if existing.exists():
                try:
                    max_id = max(int(t.teacher_id) for t in existing if t.teacher_id.isdigit())
                    new_id = str(max_id + 1)
                except Exception:
                    new_id = str(Teacher.objects.count() + 201)
            else:
                new_id = '201'

            teacher = Teacher.objects.create(
                teacher_id=new_id,
                name=name,
                email=email,
                spec=spec,
                exp=exp,
                status=status
            )

            # Log activity
            ActivityLog.objects.create(
                action="Teacher Registered",
                details=f"Registered new teacher: {name} (Spec: {spec})"
            )

            return JsonResponse({'id': teacher.id, 'teacher_id': teacher.teacher_id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@admin_api_required
@require_http_methods(["GET", "PUT", "DELETE"])
def api_teacher_detail(request, pk):
    try:
        teacher = Teacher.objects.get(pk=pk)
    except Teacher.DoesNotExist:
        return JsonResponse({'error': 'Teacher not found'}, status=404)

    if request.method == "GET":
        return JsonResponse({
            'id': teacher.id,
            'teacher_id': teacher.teacher_id,
            'name': teacher.name,
            'email': teacher.email,
            'spec': teacher.spec,
            'exp': teacher.exp,
            'status': teacher.status
        })

    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            teacher.name = data.get('name', teacher.name).strip()
            teacher.email = data.get('email', teacher.email).strip()
            teacher.spec = data.get('spec', teacher.spec).strip()
            teacher.exp = data.get('exp', teacher.exp).strip()
            teacher.status = data.get('status', teacher.status)
            teacher.save()

            # Log activity
            ActivityLog.objects.create(
                action="Teacher Updated",
                details=f"Updated profile for teacher: {teacher.name}"
            )

            return JsonResponse({'message': 'Teacher updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == "DELETE":
        name = teacher.name
        teacher.delete()

        # Log activity
        ActivityLog.objects.create(
            action="Teacher Removed",
            details=f"Removed profile of teacher: {name}"
        )

        return JsonResponse({'message': 'Teacher deleted successfully'})


# ==========================================
# Course API Views
# ==========================================
@admin_api_required
@require_http_methods(["GET", "POST"])
def api_courses(request):
    if request.method == "GET":
        courses = Course.objects.all().order_by('id')
        course_list = list(courses.values('id', 'course_id', 'title', 'teacher', 'category', 'duration', 'status'))
        return JsonResponse({'courses': course_list})

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            title = data.get('title', '').strip()
            teacher = data.get('teacher', '').strip()
            category = data.get('category', '').strip()
            duration = data.get('duration', '').strip()
            status = data.get('status', 'Active')

            if not title or not teacher or not category or not duration:
                return JsonResponse({'error': 'All fields are required'}, status=400)

            # Generate course_id
            existing = Course.objects.all()
            if existing.exists():
                try:
                    max_id = max(int(c.course_id) for c in existing if c.course_id.isdigit())
                    new_id = str(max_id + 1)
                except Exception:
                    new_id = str(Course.objects.count() + 1001)
            else:
                new_id = '1001'

            course = Course.objects.create(
                course_id=new_id,
                title=title,
                teacher=teacher,
                category=category,
                duration=duration,
                status=status
            )

            # Log activity
            ActivityLog.objects.create(
                action="Course Created",
                details=f"Created new course: {title} (Instructor: {teacher})"
            )

            return JsonResponse({'id': course.id, 'course_id': course.course_id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@admin_api_required
@require_http_methods(["GET", "PUT", "DELETE"])
def api_course_detail(request, pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return JsonResponse({'error': 'Course not found'}, status=404)

    if request.method == "GET":
        return JsonResponse({
            'id': course.id,
            'course_id': course.course_id,
            'title': course.title,
            'teacher': course.teacher,
            'category': course.category,
            'duration': course.duration,
            'status': course.status
        })

    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            course.title = data.get('title', course.title).strip()
            course.teacher = data.get('teacher', course.teacher).strip()
            course.category = data.get('category', course.category).strip()
            course.duration = data.get('duration', course.duration).strip()
            course.status = data.get('status', course.status)
            course.save()

            # Log activity
            ActivityLog.objects.create(
                action="Course Updated",
                details=f"Updated details for course: {course.title}"
            )

            return JsonResponse({'message': 'Course updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == "DELETE":
        title = course.title
        course.delete()

        # Log activity
        ActivityLog.objects.create(
            action="Course Removed",
            details=f"Deleted course: {title}"
        )

        return JsonResponse({'message': 'Course deleted successfully'})


# ==========================================
# Dashboard & logs API Views
# ==========================================
@admin_api_required
@require_http_methods(["GET"])
def api_dashboard_stats(request):
    student_count = Student.objects.count()
    teacher_count = Teacher.objects.count()
    course_count = Course.objects.count()
    return JsonResponse({
        'student_count': student_count,
        'teacher_count': teacher_count,
        'course_count': course_count
    })

@admin_api_required
@require_http_methods(["GET", "POST", "DELETE"])
def api_logs(request):
    if request.method == "GET":
        logs = ActivityLog.objects.all().order_by('-timestamp')[:25]
        log_list = []
        for l in logs:
            # Format timestamp nicely as HH:MM:SS
            # Since stored in database as UTC, convert to local string
            timestamp_str = l.timestamp.strftime('%I:%M:%S %p')
            log_list.append({
                'action': l.action,
                'details': l.details,
                'timestamp': timestamp_str
            })
        return JsonResponse({'logs': log_list})

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            action = data.get('action', '').strip()
            details = data.get('details', '').strip()

            if not action or not details:
                return JsonResponse({'error': 'Action and details are required'}, status=400)

            log = ActivityLog.objects.create(action=action, details=details)
            return JsonResponse({'message': 'Log saved'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == "DELETE":
        ActivityLog.objects.all().delete()
        # Log this action
        ActivityLog.objects.create(
            action="Logs Cleared",
            details="Admin cleared all activity logs."
        )
        return JsonResponse({'message': 'Logs cleared successfully'})


# ==========================================
# Settings API Views
# ==========================================
@admin_api_required
@require_http_methods(["GET", "POST"])
def api_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "GET":
        return JsonResponse({
            'admin_name': profile.admin_name,
            'admin_email': profile.admin_email,
            'admin_avatar': profile.admin_avatar
        })

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            # Check if updating profile text or avatar
            if 'admin_name' in data and 'admin_email' in data:
                profile.admin_name = data.get('admin_name', profile.admin_name).strip()
                profile.admin_email = data.get('admin_email', profile.admin_email).strip()
                # Also update user profile properties if needed
                request.user.first_name = profile.admin_name
                request.user.email = profile.admin_email
                request.user.save()
                log_details = f"Display name updated to: {profile.admin_name}"
                log_action = "Profile Saved"
            elif 'admin_avatar' in data:
                profile.admin_avatar = data.get('admin_avatar')
                log_details = "Uploaded new custom display photo"
                log_action = "Profile Avatar Updated"
            else:
                return JsonResponse({'error': 'Invalid profile update content'}, status=400)

            profile.save()

            ActivityLog.objects.create(
                action=log_action,
                details=log_details
            )

            return JsonResponse({'message': 'Profile updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@admin_api_required
@require_http_methods(["POST"])
def api_theme(request):
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        data = json.loads(request.body)

        profile.theme = data.get('theme', profile.theme)
        profile.accent_color = data.get('accentColor', profile.accent_color)
        profile.accent_hover = data.get('accentHover', profile.accent_hover)
        profile.save()

        ActivityLog.objects.create(
            action="Appearance Changed",
            details=f"Accent set to {profile.accent_color} and Theme set to {profile.theme.upper()}"
        )

        return JsonResponse({'message': 'Theme applied successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@admin_api_required
@require_http_methods(["POST"])
def api_notifications(request):
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        data = json.loads(request.body)

        profile.notif_email = data.get('email', profile.notif_email)
        profile.notif_student = data.get('student', profile.notif_student)
        profile.notif_digest = data.get('digest', profile.notif_digest)
        profile.save()

        ActivityLog.objects.create(
            action="Preferences Saved",
            details="Updated notification alerts preferences"
        )

        return JsonResponse({'message': 'Notifications saved successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@require_http_methods(["POST"])
def api_change_password(request):
    try:
        data = json.loads(request.body)
        current_pass = data.get('current', '')
        new_pass = data.get('newPass', '')

        user = request.user
        if not user.check_password(current_pass):
            return JsonResponse({'error': 'Current password does not match'}, status=400)

        if len(new_pass) < 6:
            return JsonResponse({'error': 'Password must be at least 6 characters'}, status=400)

        user.set_password(new_pass)
        user.save()
        
        # Keep user logged in after password change
        login(request, user)

        ActivityLog.objects.create(
            action="Security Updated",
            details="System administrator password credentials modified"
        )

        return JsonResponse({'message': 'Password updated successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ==========================================
# Backup & reset API Views
# ==========================================
@admin_api_required
@require_http_methods(["GET"])
def api_backup_export(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    students = list(Student.objects.all().values('student_id', 'name', 'email', 'course', 'status'))
    teachers = list(Teacher.objects.all().values('teacher_id', 'name', 'email', 'spec', 'exp', 'status'))
    courses = list(Course.objects.all().values('course_id', 'title', 'teacher', 'category', 'duration', 'status'))

    state = {
        'students': students,
        'teachers': teachers,
        'courses': courses,
        'preferences': {
            'theme': profile.theme,
            'accentColor': profile.accent_color,
            'accentHover': profile.accent_hover,
            'adminName': profile.admin_name,
            'adminEmail': profile.admin_email,
            'adminAvatar': profile.admin_avatar
        }
    }

    # Add log of this event
    ActivityLog.objects.create(
        action="Backup Exported",
        details="Successfully downloaded student_dashboard_backup.json"
    )

    return JsonResponse(state)

@admin_api_required
@require_http_methods(["POST"])
def api_backup_import(request):
    try:
        data = json.loads(request.body)

        # Clear existing models and import
        if 'students' in data and data['students'] is not None:
            Student.objects.all().delete()
            for s in data['students']:
                Student.objects.create(
                    student_id=s.get('student_id'),
                    name=s.get('name'),
                    email=s.get('email'),
                    course=s.get('course'),
                    status=s.get('status', 'Active')
                )

        if 'teachers' in data and data['teachers'] is not None:
            Teacher.objects.all().delete()
            for t in data['teachers']:
                Teacher.objects.create(
                    teacher_id=t.get('teacher_id'),
                    name=t.get('name'),
                    email=t.get('email'),
                    spec=t.get('spec'),
                    exp=t.get('exp'),
                    status=t.get('status', 'Active')
                )

        if 'courses' in data and data['courses'] is not None:
            Course.objects.all().delete()
            for c in data['courses']:
                Course.objects.create(
                    course_id=c.get('course_id'),
                    title=c.get('title'),
                    teacher=c.get('teacher'),
                    category=c.get('category'),
                    duration=c.get('duration'),
                    status=c.get('status', 'Active')
                )

        if 'preferences' in data and data['preferences'] is not None:
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            pref = data['preferences']
            profile.theme = pref.get('theme', profile.theme)
            profile.accent_color = pref.get('accentColor', profile.accent_color)
            profile.accent_hover = pref.get('accentHover', profile.accent_hover)
            profile.admin_name = pref.get('adminName', profile.admin_name)
            profile.admin_email = pref.get('adminEmail', profile.admin_email)
            profile.admin_avatar = pref.get('adminAvatar', profile.admin_avatar)
            profile.save()

            # Sync User properties
            request.user.first_name = profile.admin_name
            request.user.email = profile.admin_email
            request.user.save()

        ActivityLog.objects.create(
            action="Backup Imported",
            details="Uploaded and applied new student_dashboard_backup.json system state"
        )

        return JsonResponse({'message': 'Backup imported successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@admin_api_required
@require_http_methods(["POST"])
def api_reset(request):
    try:
        Student.objects.all().delete()
        Teacher.objects.all().delete()
        Course.objects.all().delete()
        ActivityLog.objects.all().delete()
        
        # Reset UserProfile settings
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile.theme = 'light'
        profile.accent_color = '#2563eb'
        profile.accent_hover = '#1d4ed8'
        profile.admin_name = 'Admin'
        profile.admin_email = 'admin@gmail.com'
        profile.admin_avatar = 'srikanth.png'
        profile.notif_email = True
        profile.notif_student = True
        profile.notif_digest = False
        profile.save()

        # Seed defaults
        seed_default_data()

        return JsonResponse({'message': 'Database reset successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ==========================================
# Admin Content Management APIs
# ==========================================
@admin_api_required
@require_http_methods(["GET", "POST"])
def api_admin_lms(request):
    if request.method == "GET":
        materials = LearningMaterial.objects.all().order_by('-uploaded_at')
        material_list = []
        for m in materials:
            material_list.append({
                'id': m.id,
                'title': m.title,
                'material_type': m.material_type,
                'material_type_display': m.get_material_type_display(),
                'file_type': m.file_type,
                'file_url': m.file_url,
                'content': m.content,
                'course_name': m.course_name,
                'description': m.description,
                'technology': m.technology,
                'batch_id': m.batch.id if m.batch else '',
                'batch_name': m.batch.name if m.batch else 'Global',
                'uploaded_at': m.uploaded_at.strftime('%Y-%m-%d %H:%M')
            })
        return JsonResponse({'materials': material_list})

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            title = data.get('title', '').strip()
            material_type = data.get('material_type', 'technical_notes').strip()
            file_type = data.get('file_type', 'PDF').strip()
            file_url = data.get('file_url', '').strip()
            content = data.get('content', '').strip()
            course_name = data.get('course_name', '').strip()
            description = data.get('description', '').strip()
            technology = data.get('technology', '').strip()
            batch_id = data.get('batch_id')

            if not title or not course_name:
                return JsonResponse({'error': 'Title and Course Name are required'}, status=400)

            batch = None
            if batch_id:
                batch = Batch.objects.filter(pk=batch_id).first()

            material = LearningMaterial.objects.create(
                title=title,
                material_type=material_type,
                file_type=file_type,
                file_url=file_url,
                content=content,
                course_name=course_name,
                description=description,
                technology=technology,
                batch=batch
            )

            ActivityLog.objects.create(
                action="LMS Material Created",
                details=f"Added LMS material: {material.title} for course {material.course_name}"
            )
            return JsonResponse({'message': 'LMS material created successfully', 'id': material.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@admin_api_required
@require_http_methods(["GET", "PUT", "DELETE"])
def api_admin_lms_detail(request, pk):
    try:
        material = LearningMaterial.objects.get(pk=pk)
    except LearningMaterial.DoesNotExist:
        return JsonResponse({'error': 'Learning material not found'}, status=404)

    if request.method == "GET":
        return JsonResponse({
            'id': material.id,
            'title': material.title,
            'material_type': material.material_type,
            'file_type': material.file_type,
            'file_url': material.file_url,
            'content': material.content,
            'course_name': material.course_name,
            'description': material.description,
            'technology': material.technology,
            'batch_id': material.batch.id if material.batch else '',
            'batch_name': material.batch.name if material.batch else 'Global'
        })

    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            material.title = data.get('title', material.title).strip()
            material.material_type = data.get('material_type', material.material_type).strip()
            material.file_type = data.get('file_type', material.file_type).strip()
            material.file_url = data.get('file_url', material.file_url).strip()
            material.content = data.get('content', material.content).strip()
            material.course_name = data.get('course_name', material.course_name).strip()
            material.description = data.get('description', material.description).strip()
            material.technology = data.get('technology', material.technology).strip()

            batch_id = data.get('batch_id')
            if batch_id:
                material.batch = Batch.objects.filter(pk=batch_id).first()
            else:
                material.batch = None

            material.save()

            ActivityLog.objects.create(
                action="LMS Material Updated",
                details=f"Updated LMS material: {material.title}"
            )
            return JsonResponse({'message': 'LMS material updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == "DELETE":
        title = material.title
        material.delete()
        ActivityLog.objects.create(
            action="LMS Material Deleted",
            details=f"Deleted LMS material: {title}"
        )
        return JsonResponse({'message': 'LMS material deleted successfully'})


@admin_api_required
@require_http_methods(["GET", "POST"])
def api_admin_mcq(request):
    if request.method == "GET":
        mcqs = MCQ.objects.all().order_by('-id')
        mcq_list = []
        for q in mcqs:
            mcq_list.append({
                'id': q.id,
                'category': q.category,
                'question_text': q.question_text,
                'option_a': q.option_a,
                'option_b': q.option_b,
                'option_c': q.option_c,
                'option_d': q.option_d,
                'correct_option': q.correct_option,
                'explanation': q.explanation,
                'difficulty': q.difficulty,
                'is_active': q.is_active
            })
        return JsonResponse({'mcqs': mcq_list})

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            category = data.get('category', '').strip()
            question_text = data.get('question_text', '').strip()
            option_a = data.get('option_a', '').strip()
            option_b = data.get('option_b', '').strip()
            option_c = data.get('option_c', '').strip()
            option_d = data.get('option_d', '').strip()
            correct_option = data.get('correct_option', '').strip()
            explanation = data.get('explanation', '').strip()
            difficulty = data.get('difficulty', 'Medium').strip()
            is_active = data.get('is_active', True)

            if not category or not question_text or not correct_option:
                return JsonResponse({'error': 'Category, Question text, and Correct option are required'}, status=400)

            q = MCQ.objects.create(
                category=category,
                question_text=question_text,
                option_a=option_a,
                option_b=option_b,
                option_c=option_c,
                option_d=option_d,
                correct_option=correct_option,
                explanation=explanation,
                difficulty=difficulty,
                is_active=is_active
            )

            ActivityLog.objects.create(
                action="MCQ Created",
                details=f"Added MCQ to category {q.category}: {q.question_text[:50]}..."
            )
            return JsonResponse({'message': 'MCQ created successfully', 'id': q.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@admin_api_required
@require_http_methods(["GET", "PUT", "DELETE"])
def api_admin_mcq_detail(request, pk):
    try:
        q = MCQ.objects.get(pk=pk)
    except MCQ.DoesNotExist:
        return JsonResponse({'error': 'MCQ not found'}, status=404)

    if request.method == "GET":
        return JsonResponse({
            'id': q.id,
            'category': q.category,
            'question_text': q.question_text,
            'option_a': q.option_a,
            'option_b': q.option_b,
            'option_c': q.option_c,
            'option_d': q.option_d,
            'correct_option': q.correct_option,
            'explanation': q.explanation,
            'difficulty': q.difficulty,
            'is_active': q.is_active
        })

    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            q.category = data.get('category', q.category).strip()
            q.question_text = data.get('question_text', q.question_text).strip()
            q.option_a = data.get('option_a', q.option_a).strip()
            q.option_b = data.get('option_b', q.option_b).strip()
            q.option_c = data.get('option_c', q.option_c).strip()
            q.option_d = data.get('option_d', q.option_d).strip()
            q.correct_option = data.get('correct_option', q.correct_option).strip()
            q.explanation = data.get('explanation', q.explanation).strip()
            q.difficulty = data.get('difficulty', q.difficulty).strip()
            q.is_active = data.get('is_active', q.is_active)
            q.save()

            ActivityLog.objects.create(
                action="MCQ Updated",
                details=f"Updated MCQ: {q.question_text[:50]}..."
            )
            return JsonResponse({'message': 'MCQ updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == "DELETE":
        q_text = q.question_text[:50]
        q.delete()
        ActivityLog.objects.create(
            action="MCQ Deleted",
            details=f"Deleted MCQ: {q_text}..."
        )
        return JsonResponse({'message': 'MCQ deleted successfully'})


@admin_api_required
@require_http_methods(["GET", "POST"])
def api_admin_coding(request):
    if request.method == "GET":
        challenges = CodingChallenge.objects.all().order_by('-id')
        challenge_list = []
        for c in challenges:
            challenge_list.append({
                'id': c.id,
                'title': c.title,
                'difficulty': c.difficulty,
                'description': c.description,
                'input_format': c.input_format,
                'output_format': c.output_format,
                'sample_input': c.sample_input,
                'sample_output': c.sample_output,
                'sample_solution': c.sample_solution,
                'show_solution_to_students': c.show_solution_to_students,
                'category': c.category,
                'topic': c.topic,
                'technology': c.technology
            })
        return JsonResponse({'challenges': challenge_list})

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            title = data.get('title', '').strip()
            difficulty = data.get('difficulty', 'Medium').strip()
            description = data.get('description', '').strip()
            input_format = data.get('input_format', '').strip()
            output_format = data.get('output_format', '').strip()
            sample_input = data.get('sample_input', '').strip()
            sample_output = data.get('sample_output', '').strip()
            sample_solution = data.get('sample_solution', '').strip()
            show_solution_to_students = data.get('show_solution_to_students', True)
            category = data.get('category', 'Python').strip()
            topic = data.get('topic', '').strip()
            technology = data.get('technology', '').strip()

            if not title or not description:
                return JsonResponse({'error': 'Title and Description are required'}, status=400)

            c = CodingChallenge.objects.create(
                title=title,
                difficulty=difficulty,
                description=description,
                input_format=input_format,
                output_format=output_format,
                sample_input=sample_input,
                sample_output=sample_output,
                sample_solution=sample_solution,
                show_solution_to_students=show_solution_to_students,
                category=category,
                topic=topic,
                technology=technology
            )

            ActivityLog.objects.create(
                action="Coding Challenge Created",
                details=f"Added coding challenge: {c.title} ({c.difficulty})"
            )
            return JsonResponse({'message': 'Coding challenge created successfully', 'id': c.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@admin_api_required
@require_http_methods(["GET", "PUT", "DELETE"])
def api_admin_coding_detail(request, pk):
    try:
        c = CodingChallenge.objects.get(pk=pk)
    except CodingChallenge.DoesNotExist:
        return JsonResponse({'error': 'Coding challenge not found'}, status=404)

    if request.method == "GET":
        return JsonResponse({
            'id': c.id,
            'title': c.title,
            'difficulty': c.difficulty,
            'description': c.description,
            'input_format': c.input_format,
            'output_format': c.output_format,
            'sample_input': c.sample_input,
            'sample_output': c.sample_output,
            'sample_solution': c.sample_solution,
            'show_solution_to_students': c.show_solution_to_students,
            'category': c.category,
            'topic': c.topic,
            'technology': c.technology
        })

    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            c.title = data.get('title', c.title).strip()
            c.difficulty = data.get('difficulty', c.difficulty).strip()
            c.description = data.get('description', c.description).strip()
            c.input_format = data.get('input_format', c.input_format).strip()
            c.output_format = data.get('output_format', c.output_format).strip()
            c.sample_input = data.get('sample_input', c.sample_input).strip()
            c.sample_output = data.get('sample_output', c.sample_output).strip()
            c.sample_solution = data.get('sample_solution', c.sample_solution).strip()
            c.show_solution_to_students = data.get('show_solution_to_students', c.show_solution_to_students)
            c.category = data.get('category', c.category).strip()
            c.topic = data.get('topic', c.topic).strip()
            c.technology = data.get('technology', c.technology).strip()
            c.save()

            ActivityLog.objects.create(
                action="Coding Challenge Updated",
                details=f"Updated coding challenge: {c.title}"
            )
            return JsonResponse({'message': 'Coding challenge updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == "DELETE":
        title = c.title
        c.delete()
        ActivityLog.objects.create(
            action="Coding Challenge Deleted",
            details=f"Deleted coding challenge: {title}"
        )
        return JsonResponse({'message': 'Coding challenge deleted successfully'})


@admin_api_required
@require_http_methods(["GET", "POST"])
def api_admin_schedule(request):
    if request.method == "GET":
        schedules = ClassSchedule.objects.all().order_by('-id')
        schedule_list = []
        for s in schedules:
            schedule_list.append({
                'id': s.id,
                'batch_id': s.batch.id if s.batch else '',
                'batch_name': s.batch.name if s.batch else 'Global',
                'course_name': s.course_name,
                'day': s.day,
                'subject': s.subject,
                'faculty': s.faculty,
                'start_time': s.start_time,
                'end_time': s.end_time,
                'meeting_link': s.meeting_link,
                'notes': s.notes
            })
        return JsonResponse({'schedules': schedule_list})

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            batch_id = data.get('batch_id')
            course_name = data.get('course_name', '').strip()
            day = data.get('day', '').strip()
            subject = data.get('subject', '').strip()
            faculty = data.get('faculty', '').strip()
            start_time = data.get('start_time', '').strip()
            end_time = data.get('end_time', '').strip()
            meeting_link = data.get('meeting_link', '').strip()
            notes = data.get('notes', '').strip()

            if not course_name or not day or not subject or not faculty or not start_time or not end_time:
                return JsonResponse({'error': 'Course name, Day, Subject, Faculty, Start time, and End time are required'}, status=400)

            batch = None
            if batch_id:
                batch = Batch.objects.filter(pk=batch_id).first()

            s = ClassSchedule.objects.create(
                batch=batch,
                course_name=course_name,
                day=day,
                subject=subject,
                faculty=faculty,
                start_time=start_time,
                end_time=end_time,
                meeting_link=meeting_link,
                notes=notes
            )

            ActivityLog.objects.create(
                action="Class Schedule Created",
                details=f"Scheduled class: {s.subject} ({s.day} {s.start_time}-{s.end_time})"
            )
            return JsonResponse({'message': 'Class schedule created successfully', 'id': s.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@admin_api_required
@require_http_methods(["GET", "PUT", "DELETE"])
def api_admin_schedule_detail(request, pk):
    try:
        s = ClassSchedule.objects.get(pk=pk)
    except ClassSchedule.DoesNotExist:
        return JsonResponse({'error': 'Class schedule not found'}, status=404)

    if request.method == "GET":
        return JsonResponse({
            'id': s.id,
            'batch_id': s.batch.id if s.batch else '',
            'batch_name': s.batch.name if s.batch else 'Global',
            'course_name': s.course_name,
            'day': s.day,
            'subject': s.subject,
            'faculty': s.faculty,
            'start_time': s.start_time,
            'end_time': s.end_time,
            'meeting_link': s.meeting_link,
            'notes': s.notes
        })

    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            s.course_name = data.get('course_name', s.course_name).strip()
            s.day = data.get('day', s.day).strip()
            s.subject = data.get('subject', s.subject).strip()
            s.faculty = data.get('faculty', s.faculty).strip()
            s.start_time = data.get('start_time', s.start_time).strip()
            s.end_time = data.get('end_time', s.end_time).strip()
            s.meeting_link = data.get('meeting_link', s.meeting_link).strip()
            s.notes = data.get('notes', s.notes).strip()

            batch_id = data.get('batch_id')
            if batch_id:
                s.batch = Batch.objects.filter(pk=batch_id).first()
            else:
                s.batch = None

            s.save()

            ActivityLog.objects.create(
                action="Class Schedule Updated",
                details=f"Updated class schedule: {s.subject} ({s.day})"
            )
            return JsonResponse({'message': 'Class schedule updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == "DELETE":
        details = f"{s.subject} ({s.day})"
        s.delete()
        ActivityLog.objects.create(
            action="Class Schedule Deleted",
            details=f"Deleted class schedule: {details}"
        )
        return JsonResponse({'message': 'Class schedule deleted successfully'})


@admin_api_required
@require_http_methods(["GET", "POST"])
def api_admin_assignments(request):
    if request.method == "GET":
        assignments = Assignment.objects.all().order_by('-created_at')
        assignment_list = []
        for a in assignments:
            assignment_list.append({
                'id': a.id,
                'title': a.title,
                'description': a.description,
                'course_name': a.course_name,
                'due_date': a.due_date,
                'technology': a.technology,
                'batch_id': a.batch.id if a.batch else '',
                'batch_name': a.batch.name if a.batch else 'Global',
                'file_url': a.file_url,
                'marks': a.marks,
                'instructions': a.instructions,
                'is_published': a.is_published,
                'created_at': a.created_at.strftime('%Y-%m-%d')
            })
        return JsonResponse({'assignments': assignment_list})

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            title = data.get('title', '').strip()
            description = data.get('description', '').strip()
            course_name = data.get('course_name', '').strip()
            due_date = data.get('due_date', '').strip()
            technology = data.get('technology', '').strip()
            batch_id = data.get('batch_id')
            file_url = data.get('file_url', '').strip()
            marks = int(data.get('marks', 100))
            instructions = data.get('instructions', '').strip()
            is_published = data.get('is_published', True)

            if not title or not course_name or not due_date:
                return JsonResponse({'error': 'Title, Course Name, and Due Date are required'}, status=400)

            batch = None
            if batch_id:
                batch = Batch.objects.filter(pk=batch_id).first()

            a = Assignment.objects.create(
                title=title,
                description=description,
                course_name=course_name,
                due_date=due_date,
                technology=technology,
                batch=batch,
                file_url=file_url,
                marks=marks,
                instructions=instructions,
                is_published=is_published
            )

            ActivityLog.objects.create(
                action="Assignment Created",
                details=f"Created assignment: {a.title} ({a.course_name})"
            )
            return JsonResponse({'message': 'Assignment created successfully', 'id': a.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@admin_api_required
@require_http_methods(["GET", "PUT", "DELETE"])
def api_admin_assignments_detail(request, pk):
    try:
        a = Assignment.objects.get(pk=pk)
    except Assignment.DoesNotExist:
        return JsonResponse({'error': 'Assignment not found'}, status=404)

    if request.method == "GET":
        return JsonResponse({
            'id': a.id,
            'title': a.title,
            'description': a.description,
            'course_name': a.course_name,
            'due_date': a.due_date,
            'technology': a.technology,
            'batch_id': a.batch.id if a.batch else '',
            'batch_name': a.batch.name if a.batch else 'Global',
            'file_url': a.file_url,
            'marks': a.marks,
            'instructions': a.instructions,
            'is_published': a.is_published
        })

    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            a.title = data.get('title', a.title).strip()
            a.description = data.get('description', a.description).strip()
            a.course_name = data.get('course_name', a.course_name).strip()
            a.due_date = data.get('due_date', a.due_date).strip()
            a.technology = data.get('technology', a.technology).strip()
            a.file_url = data.get('file_url', a.file_url).strip()
            a.marks = int(data.get('marks', a.marks))
            a.instructions = data.get('instructions', a.instructions).strip()
            a.is_published = data.get('is_published', a.is_published)

            batch_id = data.get('batch_id')
            if batch_id:
                a.batch = Batch.objects.filter(pk=batch_id).first()
            else:
                a.batch = None

            a.save()

            ActivityLog.objects.create(
                action="Assignment Updated",
                details=f"Updated assignment: {a.title}"
            )
            return JsonResponse({'message': 'Assignment updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == "DELETE":
        title = a.title
        a.delete()
        ActivityLog.objects.create(
            action="Assignment Deleted",
            details=f"Deleted assignment: {title}"
        )
        return JsonResponse({'message': 'Assignment deleted successfully'})


# ==========================================
# Student Portal Access Control Decorators
# ==========================================
def student_page_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not hasattr(request.user, 'student_profile'):
            return redirect('index')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def student_api_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not hasattr(request.user, 'student_profile'):
            return JsonResponse({'error': 'Unauthorized: Access denied'}, status=403)
        return view_func(request, *args, **kwargs)
    return _wrapped_view


# ==========================================
# Student Portal Page Views
# ==========================================
@student_page_required
@ensure_csrf_cookie
def student_dashboard_view(request):
    seed_default_data()
    return render(request, 'student_dashboard.html')

@student_page_required
@ensure_csrf_cookie
def student_profile_view(request):
    return render(request, 'student_profile.html')

@student_page_required
@ensure_csrf_cookie
def student_lms_view(request):
    return render(request, 'student_lms.html')

@student_page_required
@ensure_csrf_cookie
def student_mcq_view(request):
    return render(request, 'student_mcq.html')

@student_page_required
@ensure_csrf_cookie
def student_coding_view(request):
    return render(request, 'student_coding.html')

@student_page_required
@ensure_csrf_cookie
def student_schedule_view(request):
    return render(request, 'student_schedule.html')

@student_page_required
@ensure_csrf_cookie
def student_assignments_view(request):
    return render(request, 'student_assignments.html')


# ==========================================
# Student Portal Helper Functions
# ==========================================
def generate_weekly_schedule_for_course(course_name):
    today = date.today()
    year, week_num, day_of_week = today.isocalendar()
    
    random.seed(f"{course_name}-{year}-{week_num}")
    
    subjects_dict = {
        'Python Full Stack': ['Python Core', 'Django Framework', 'HTML/CSS Basics', 'JavaScript', 'Database & SQL', 'REST APIs', 'Git & Deployment'],
        'Java Development': ['Java Core', 'Spring Boot', 'Hibernate ORM', 'SQL & Database Design', 'Microservices', 'Data Structures', 'System Design'],
        'Web Development': ['HTML5 & CSS3', 'JavaScript Essentials', 'React JS', 'Tailwind CSS', 'UI/UX Principles', 'Web Performance', 'SEO Basics'],
        'React JS': ['ES6+ Javascript', 'React Components & Props', 'React Hooks', 'State Management (Redux)', 'React Router', 'API Integration', 'Testing React'],
        'Flutter Mobile App': ['Dart Programming', 'Flutter Widgets', 'State Management', 'Firebase Integration', 'REST APIs in Flutter', 'App Store Publishing', 'Custom Animations']
    }
    
    course_subjects = subjects_dict.get(course_name, ['Technical Theory', 'Core Concepts', 'Soft Skills', 'Aptitude Practice'])
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    schedule_data = []
    
    overrides = WeeklyScheduleOverride.objects.filter(course_name=course_name)
    
    for day in days:
        tech_class_1 = random.choice(course_subjects)
        tech_class_2 = random.choice(course_subjects)
        while tech_class_2 == tech_class_1 and len(course_subjects) > 1:
            tech_class_2 = random.choice(course_subjects)
            
        slots = [
            {'time': '09:30 AM – 11:30 AM', 'type': 'Technical Class', 'title': tech_class_1, 'desc': 'Interactive live session & concepts'},
            {'time': '11:30 AM – 12:30 PM', 'type': 'Preparation / Practice', 'title': f'Practice: {tech_class_1}', 'desc': 'Self-preparation and coding exercises'},
            {'time': '12:30 PM – 12:45 PM', 'type': 'Short Break', 'title': 'Short Break', 'desc': '15-minute quick break'},
            {'time': '01:00 PM – 02:00 PM', 'type': 'Lunch Break', 'title': 'Lunch Break', 'desc': 'Fixed lunch break'},
            {'time': '02:00 PM – 04:00 PM', 'type': 'Technical Class', 'title': tech_class_2, 'desc': 'Hands-on practical development'},
            {'time': '04:00 PM – 04:30 PM', 'type': 'Daily Revision / Assignment', 'title': 'Daily Assignment', 'desc': 'Recap and tasks evaluation'}
        ]
        
        # Apply overrides if they match this day
        day_overrides = overrides.filter(day_of_week=day)
        for o in day_overrides:
            for s in slots:
                if s['time'].lower().replace(' ', '').replace('–', '-') == o.time_slot.lower().replace(' ', '').replace('–', '-'):
                    s['type'] = o.activity_type
                    s['title'] = o.subject
                    s['desc'] = f"Instructor: {o.instructor}"
                    
        schedule_data.append({
            'day': day,
            'slots': slots
        })
    return schedule_data

def recalculate_student_progress(profile):
    total_challenges = CodingChallenge.objects.count()
    completed_challenges = CodingChallengeSubmission.objects.filter(student=profile, status='Completed').values('challenge').distinct().count()
    
    total_categories = 9
    attempted_categories = MCQAttempt.objects.filter(student=profile).values('category').distinct().count()
    
    total_assignments = Assignment.objects.filter(course_name=profile.course_name).count()
    completed_assignments = AssignmentSubmission.objects.filter(student=profile, status='Submitted').values('assignment').distinct().count()
    
    challenge_factor = (completed_challenges / total_challenges) if total_challenges > 0 else 0
    mcq_factor = (attempted_categories / total_categories)
    assignment_factor = (completed_assignments / total_assignments) if total_assignments > 0 else 0
    
    percentage = int((challenge_factor * 40) + (mcq_factor * 40) + (assignment_factor * 20))
    percentage = min(percentage, 100)
    
    progress, created = StudentProgress.objects.get_or_create(student=profile)
    progress.completion_percentage = percentage
    progress.save()
    return percentage


# ==========================================
# Student Portal REST API Views
# ==========================================
@student_api_required
@require_http_methods(["GET", "POST"])
def api_student_profile(request):
    profile = request.user.student_profile
    if request.method == "GET":
        return JsonResponse({
            'full_name': profile.full_name,
            'student_id': profile.student_id,
            'email': profile.email,
            'mobile_number': profile.mobile_number,
            'address': profile.address,
            'date_of_birth': profile.date_of_birth,
            'gender': profile.gender,
            'educational_qualification': profile.educational_qualification,
            'previous_study_details': profile.previous_study_details,
            'college_university_name': profile.college_university_name,
            'batch_name': profile.batch.name if profile.batch else (profile.batch_name or 'N/A'),
            'course_name': profile.course_name,
            'joining_date': profile.joining_date or 'N/A',
            'emergency_contact': profile.emergency_contact,
            'profile_photo': profile.profile_photo
        })
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            # Allow limited updates per guidelines
            if 'mobile_number' in data:
                profile.mobile_number = data.get('mobile_number').strip()
            if 'address' in data:
                profile.address = data.get('address').strip()
            if 'profile_photo' in data:
                profile.profile_photo = data.get('profile_photo')
            if 'date_of_birth' in data:
                profile.date_of_birth = data.get('date_of_birth').strip()
            if 'gender' in data:
                profile.gender = data.get('gender').strip()
            if 'educational_qualification' in data:
                profile.educational_qualification = data.get('educational_qualification').strip()
            if 'previous_study_details' in data:
                profile.previous_study_details = data.get('previous_study_details').strip()
            if 'college_university_name' in data:
                profile.college_university_name = data.get('college_university_name').strip()
            if 'emergency_contact' in data:
                profile.emergency_contact = data.get('emergency_contact').strip()
            
            profile.save()
            return JsonResponse({'message': 'Profile updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@student_api_required
@require_http_methods(["GET"])
def api_student_lms(request):
    profile = request.user.student_profile
    materials = LearningMaterial.objects.filter(
        Q(course_name=profile.course_name) & 
        (Q(batch=profile.batch) | Q(batch__isnull=True))
    ).order_by('uploaded_at')
    
    # Format choice values
    material_list = []
    for m in materials:
        material_list.append({
            'id': m.id,
            'title': m.title,
            'material_type': m.get_material_type_display(),
            'file_type': m.file_type,
            'file_url': m.file_url,
            'content': m.content,
            'uploaded_at': m.uploaded_at.strftime('%Y-%m-%d')
        })
    return JsonResponse({'materials': material_list})

@student_api_required
@require_http_methods(["GET", "POST"])
def api_student_mcq(request):
    profile = request.user.student_profile
    if request.method == "GET":
        mcqs = MCQ.objects.filter(is_active=True)
        history = MCQAttempt.objects.filter(student=profile).order_by('-attempted_at')
        
        mcq_list = []
        for q in mcqs:
            mcq_list.append({
                'id': q.id,
                'category': q.category,
                'question_text': q.question_text,
                'option_a': q.option_a,
                'option_b': q.option_b,
                'option_c': q.option_c,
                'option_d': q.option_d
            })
            
        history_list = []
        for h in history:
            history_list.append({
                'category': h.category,
                'score': h.score,
                'total': h.total_questions,
                'date': h.attempted_at.strftime('%Y-%m-%d %I:%M %p')
            })
            
        return JsonResponse({
            'mcqs': mcq_list,
            'history': history_list
        })
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            category = data.get('category')
            answers = data.get('answers') # dict of {mcq_id: selected_option}
            
            if not category or not answers:
                return JsonResponse({'error': 'Category and answers are required'}, status=400)
                
            mcqs = MCQ.objects.filter(category=category, is_active=True)
            total = mcqs.count()
            score = 0
            
            for q in mcqs:
                selected = answers.get(str(q.id))
                if selected == q.correct_option:
                    score += 1
                    
            attempt = MCQAttempt.objects.create(
                student=profile,
                category=category,
                score=score,
                total_questions=total
            )
            
            recalculate_student_progress(profile)
            
            return JsonResponse({
                'score': score,
                'total': total,
                'message': f'Quiz submitted successfully. Score: {score}/{total}'
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@student_api_required
@require_http_methods(["GET", "POST"])
def api_student_coding(request):
    profile = request.user.student_profile
    if request.method == "GET":
        challenges = CodingChallenge.objects.all().order_by('difficulty', 'id')
        submissions = CodingChallengeSubmission.objects.filter(student=profile)
        
        sub_map = {s.challenge_id: s.status for s in submissions}
        code_map = {s.challenge_id: s.code_submitted for s in submissions}
        
        challenge_list = []
        for c in challenges:
            challenge_list.append({
                'id': c.id,
                'title': c.title,
                'difficulty': c.difficulty,
                'description': c.description,
                'input_format': c.input_format,
                'output_format': c.output_format,
                'sample_input': c.sample_input,
                'sample_output': c.sample_output,
                'sample_solution': c.sample_solution if c.show_solution_to_students else '',
                'category': c.category,
                'status': sub_map.get(c.id, 'Pending'),
                'saved_code': code_map.get(c.id, '')
            })
        return JsonResponse({'challenges': challenge_list})
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            challenge_id = data.get('challenge_id')
            code = data.get('code', '')
            
            if not challenge_id:
                return JsonResponse({'error': 'Challenge ID is required'}, status=400)
                
            challenge = CodingChallenge.objects.get(pk=challenge_id)
            submission, created = CodingChallengeSubmission.objects.get_or_create(
                student=profile,
                challenge=challenge,
                defaults={'code_submitted': code, 'status': 'Completed'}
            )
            if not created:
                submission.code_submitted = code
                submission.status = 'Completed'
                submission.save()
                
            recalculate_student_progress(profile)
            return JsonResponse({'message': 'Challenge solution submitted successfully', 'status': 'Completed'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@student_api_required
@require_http_methods(["GET"])
def api_student_schedule(request):
    profile = request.user.student_profile
    q_filter = Q(batch=profile.batch) if profile.batch else Q(course_name=profile.course_name)
    schedules = ClassSchedule.objects.filter(q_filter)
    
    if schedules.exists():
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        schedule_data = []
        for day in days:
            day_schedules = schedules.filter(day=day)
            slots = []
            for s in day_schedules:
                slots.append({
                    'time': f"{s.start_time} – {s.end_time}",
                    'type': 'Technical Class',
                    'title': s.subject,
                    'desc': f"Faculty: {s.faculty}. Link: {s.meeting_link}. Notes: {s.notes}" if s.meeting_link else f"Faculty: {s.faculty}. Notes: {s.notes}"
                })
            
            # Standard slots so the timetable displays nicely
            slots.append({'time': '12:30 PM – 12:45 PM', 'type': 'Short Break', 'title': 'Short Break', 'desc': '15-minute quick break'})
            slots.append({'time': '01:00 PM – 02:00 PM', 'type': 'Lunch Break', 'title': 'Lunch Break', 'desc': 'Fixed lunch break'})
            
            schedule_data.append({
                'day': day,
                'slots': slots
            })
        return JsonResponse({'schedule': schedule_data})
        
    schedule = generate_weekly_schedule_for_course(profile.course_name)
    return JsonResponse({'schedule': schedule})

@student_api_required
@require_http_methods(["GET", "POST"])
def api_student_assignments(request):
    profile = request.user.student_profile
    if request.method == "GET":
        q_filter = Q(course_name=profile.course_name) & (Q(batch=profile.batch) | Q(batch__isnull=True))
        assignments = Assignment.objects.filter(q_filter, is_published=True).order_by('-created_at')
        submissions = AssignmentSubmission.objects.filter(student=profile)
        
        sub_map = {s.assignment_id: s.status for s in submissions}
        date_map = {s.assignment_id: s.submitted_at.strftime('%Y-%m-%d %I:%M %p') for s in submissions}
        content_map = {s.assignment_id: s.submission_content for s in submissions}
        
        assign_list = []
        for a in assignments:
            assign_list.append({
                'id': a.id,
                'title': a.title,
                'description': a.description,
                'due_date': a.due_date,
                'status': sub_map.get(a.id, 'Pending'),
                'submitted_at': date_map.get(a.id, ''),
                'submission_content': content_map.get(a.id, '')
            })
        return JsonResponse({'assignments': assign_list})
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            assignment_id = data.get('assignment_id')
            content = data.get('content', '').strip()
            
            if not assignment_id or not content:
                return JsonResponse({'error': 'Assignment ID and content are required'}, status=400)
                
            assignment = Assignment.objects.get(pk=assignment_id)
            submission, created = AssignmentSubmission.objects.get_or_create(
                student=profile,
                assignment=assignment,
                defaults={'submission_content': content, 'status': 'Submitted'}
            )
            if not created:
                submission.submission_content = content
                submission.status = 'Submitted'
                submission.save()
                
            recalculate_student_progress(profile)
            return JsonResponse({'message': 'Assignment submitted successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@student_api_required
@require_http_methods(["GET"])
def api_student_stats(request):
    profile = request.user.student_profile
    
    # Dynamic calculations
    progress_pct = recalculate_student_progress(profile)
    
    materials_count = LearningMaterial.objects.filter(
        Q(course_name=profile.course_name) & 
        (Q(batch=profile.batch) | Q(batch__isnull=True))
    ).count()
    
    completed_challenges = CodingChallengeSubmission.objects.filter(student=profile, status='Completed').count()
    completed_quizzes = MCQAttempt.objects.filter(student=profile).count()
    
    q_filter = Q(course_name=profile.course_name) & (Q(batch=profile.batch) | Q(batch__isnull=True))
    total_assign = Assignment.objects.filter(q_filter, is_published=True).count()
    
    sub_assign = AssignmentSubmission.objects.filter(student=profile).count()
    pending_assign = total_assign - sub_assign
    
    # Determine upcoming class (based on custom schedule or fallback)
    q_filter_sched = Q(batch=profile.batch) if profile.batch else Q(course_name=profile.course_name)
    schedules = ClassSchedule.objects.filter(q_filter_sched)
    today_name = date.today().strftime('%A')
    upcoming_class = "No classes scheduled today"
    
    if schedules.exists():
        today_schedules = schedules.filter(day=today_name)
        if today_schedules.exists():
            first_sched = today_schedules.first()
            upcoming_class = f"{first_sched.subject} ({first_sched.start_time} – {first_sched.end_time})"
    else:
        schedule = generate_weekly_schedule_for_course(profile.course_name)
        for day_sched in schedule:
            if day_sched['day'] == today_name:
                classes = [s for s in day_sched['slots'] if s['type'] == 'Technical Class']
                if classes:
                    upcoming_class = f"{classes[0]['title']} ({classes[0]['time']})"
                break
            
    return JsonResponse({
        'student_id': profile.student_id,
        'full_name': profile.full_name,
        'course_name': profile.course_name,
        'batch_name': profile.batch.name if profile.batch else (profile.batch_name or 'N/A'),
        'profile_photo': profile.profile_photo,
        'progress_percentage': progress_pct,
        'materials_count': materials_count,
        'completed_challenges': completed_challenges,
        'completed_quizzes': completed_quizzes,
        'pending_assignments': pending_assign,
        'upcoming_class': upcoming_class
    })

@student_api_required
@require_http_methods(["GET"])
def api_student_announcements(request):
    profile = request.user.student_profile
    announcements = Announcement.objects.filter(
        course_name__in=['All', profile.course_name]
    ).order_by('-created_at')[:10]
    
    ann_list = []
    for a in announcements:
        ann_list.append({
            'title': a.title,
            'content': a.content,
            'date': a.created_at.strftime('%Y-%m-%d %I:%M %p')
        })
    return JsonResponse({'announcements': ann_list})

