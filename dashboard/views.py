import json
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Student, Teacher, Course, ActivityLog, UserProfile

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

# ==========================================
# Page Views
# ==========================================
@ensure_csrf_cookie
def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'login.html')

@ensure_csrf_cookie
def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'register.html')

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return render(request, 'logout.html')

@login_required
@ensure_csrf_cookie
def index_view(request):
    seed_default_data()
    return render(request, 'index.html')

@login_required
@ensure_csrf_cookie
def student_view(request):
    return render(request, 'student.html')

@login_required
@ensure_csrf_cookie
def courses_view(request):
    return render(request, 'courses.html')

@login_required
@ensure_csrf_cookie
def teachers_view(request):
    return render(request, 'teachers.html')

@login_required
@ensure_csrf_cookie
def schedule_view(request):
    return render(request, 'schedule.html')

@login_required
@ensure_csrf_cookie
def reports_view(request):
    return render(request, 'reports.html')

@login_required
@ensure_csrf_cookie
def settings_view(request):
    return render(request, 'settings.html')


# ==========================================
# Auth API Views
# ==========================================
@require_http_methods(["POST"])
def api_login(request):
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        password = data.get('password', '')

        if not email or not password:
            return JsonResponse({'error': 'Email and Password are required'}, status=400)

        # Authenticate using username (if name differs, search for user by email first)
        username = email
        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            pass

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Log this activity
            ActivityLog.objects.create(
                action="Admin Logged In",
                details=f"User {user.username} authenticated successfully."
            )
            return JsonResponse({'message': 'Logged in successfully'})
        else:
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

        if User.objects.filter(email=email).exists():
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


# ==========================================
# Student API Views
# ==========================================
@login_required
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

@login_required
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
            student.name = data.get('name', student.name).strip()
            student.email = data.get('email', student.email).strip()
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
@login_required
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

@login_required
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
@login_required
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

@login_required
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
@login_required
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

@login_required
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
@login_required
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

@login_required
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

@login_required
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
@login_required
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

@login_required
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

@login_required
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
