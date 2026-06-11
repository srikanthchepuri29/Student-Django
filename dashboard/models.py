from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    student_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    course = models.CharField(max_length=150)
    status = models.CharField(max_length=50, default='Active')

    def __str__(self):
        return self.name

class Teacher(models.Model):
    teacher_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    spec = models.CharField(max_length=150)
    exp = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default='Active')

    def __str__(self):
        return self.name

class Course(models.Model):
    course_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=150)
    teacher = models.CharField(max_length=150)
    category = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default='Active')

    def __str__(self):
        return self.title

class ActivityLog(models.Model):
    action = models.CharField(max_length=100)
    details = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} - {self.timestamp}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    admin_name = models.CharField(max_length=150, default='Admin')
    admin_email = models.EmailField(default='admin@gmail.com')
    admin_avatar = models.TextField(default='srikanth.png') # Stored as Base64 string or filename
    theme = models.CharField(max_length=20, default='light')
    accent_color = models.CharField(max_length=20, default='#2563eb')
    accent_hover = models.CharField(max_length=20, default='#1d4ed8')
    notif_email = models.BooleanField(default=True)
    notif_student = models.BooleanField(default=True)
    notif_digest = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s profile"


# ==========================================
# Student Portal Integration Models
# ==========================================
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date

class Batch(models.Model):
    name = models.CharField(max_length=150)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='batches')
    joining_date = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.name} ({self.course.title})"

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_obj = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='profile_detail', null=True, blank=True)
    
    # Required personal details:
    full_name = models.CharField(max_length=150)
    student_id = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=20, blank=True, default='')
    address = models.TextField(blank=True, default='')
    date_of_birth = models.CharField(max_length=50, blank=True, default='')
    gender = models.CharField(max_length=20, blank=True, default='')
    educational_qualification = models.CharField(max_length=150, blank=True, default='')
    previous_study_details = models.CharField(max_length=150, blank=True, default='')
    college_university_name = models.CharField(max_length=150, blank=True, default='')
    
    # Course / Batch:
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    batch_name = models.CharField(max_length=150, blank=True, default='')
    course_name = models.CharField(max_length=150)
    joining_date = models.CharField(max_length=50, blank=True, default='')
    emergency_contact = models.CharField(max_length=20, blank=True, default='')
    profile_photo = models.TextField(default='srikanth.png')

    def __str__(self):
        return self.full_name

class LearningMaterial(models.Model):
    MATERIAL_TYPES = [
        ('technical_notes', 'Technical Notes'),
        ('aptitude', 'Aptitude Preparation'),
        ('english', 'English Communication'),
        ('interview_q', 'Technical Interview Questions'),
        ('mini_projects', 'Mini Projects'),
        ('mock_interview', 'Mock Interview Preparation'),
        ('daily_tasks', 'Daily Practice Tasks'),
    ]
    
    title = models.CharField(max_length=200)
    material_type = models.CharField(max_length=50, choices=MATERIAL_TYPES)
    file_type = models.CharField(max_length=50, default='PDF') # PDF, Video, Document, Link
    file_url = models.CharField(max_length=500, blank=True, default='')
    content = models.TextField(blank=True, default='')
    course_name = models.CharField(max_length=150)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # Added for Admin portal content management:
    description = models.TextField(blank=True, default='')
    technology = models.CharField(max_length=150, blank=True, default='')
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True, related_name='materials')

    def __str__(self):
        return f"{self.title} ({self.course_name})"

class MCQ(models.Model):
    CATEGORIES = [
        ('Python', 'Python'),
        ('HTML', 'HTML'),
        ('CSS', 'CSS'),
        ('JavaScript', 'JavaScript'),
        ('Django', 'Django'),
        ('SQL', 'SQL'),
        ('Aptitude', 'Aptitude'),
        ('English', 'English'),
        ('Logical Reasoning', 'Logical Reasoning'),
    ]
    
    category = models.CharField(max_length=50, choices=CATEGORIES)
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    
    # Added for Admin portal content management:
    explanation = models.TextField(blank=True, default='')
    difficulty = models.CharField(max_length=20, default='Medium')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.category}: {self.question_text[:50]}"

class MCQAttempt(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='mcq_attempts')
    category = models.CharField(max_length=50)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    attempted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.category}: {self.score}/{self.total_questions}"

class CodingChallenge(models.Model):
    DIFFICULTIES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]
    
    title = models.CharField(max_length=200)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTIES)
    description = models.TextField()
    input_format = models.TextField()
    output_format = models.TextField()
    sample_input = models.TextField()
    sample_output = models.TextField()
    sample_solution = models.TextField(blank=True, default='')
    show_solution_to_students = models.BooleanField(default=True)
    category = models.CharField(max_length=50, default='Python')
    
    # Added for Admin portal content management:
    topic = models.CharField(max_length=150, blank=True, default='')
    technology = models.CharField(max_length=150, blank=True, default='')
    
    def __str__(self):
        return f"{self.title} ({self.difficulty})"

class CodingChallengeSubmission(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='challenge_submissions')
    challenge = models.ForeignKey(CodingChallenge, on_delete=models.CASCADE)
    code_submitted = models.TextField()
    status = models.CharField(max_length=20, default='Completed')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.challenge.title}: {self.status}"

class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    course_name = models.CharField(max_length=150)
    due_date = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Added for Admin portal content management:
    technology = models.CharField(max_length=150, blank=True, default='')
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True, related_name='assignments')
    file_url = models.CharField(max_length=500, blank=True, default='')
    marks = models.IntegerField(default=100)
    instructions = models.TextField(blank=True, default='')
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.course_name})"

class AssignmentSubmission(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='assignment_submissions')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    submission_content = models.TextField(blank=True, default='')
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Submitted')

    def __str__(self):
        return f"{self.student.full_name} - {self.assignment.title}"

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    course_name = models.CharField(max_length=150, default='All')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class StudentProgress(models.Model):
    student = models.OneToOneField(StudentProfile, on_delete=models.CASCADE, related_name='progress')
    completion_percentage = models.IntegerField(default=0)
    last_active = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.completion_percentage}%"

class WeeklyScheduleOverride(models.Model):
    course_name = models.CharField(max_length=150)
    day_of_week = models.CharField(max_length=20)
    time_slot = models.CharField(max_length=50)
    activity_type = models.CharField(max_length=100)
    subject = models.CharField(max_length=150)
    instructor = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.course_name} - {self.day_of_week} ({self.time_slot})"


class ClassSchedule(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True, related_name='class_schedules')
    course_name = models.CharField(max_length=150)
    day = models.CharField(max_length=20)
    subject = models.CharField(max_length=150)
    faculty = models.CharField(max_length=150)
    start_time = models.CharField(max_length=20)
    end_time = models.CharField(max_length=20)
    meeting_link = models.CharField(max_length=500, blank=True, default='')
    notes = models.TextField(blank=True, default='')

    def __str__(self):
        return f"{self.course_name} - {self.subject} ({self.day})"


# ==========================================
# Signals for Automatic Student Synchronization
# ==========================================
@receiver(post_save, sender=Student)
def sync_student_profile(sender, instance, created, **kwargs):
    if created:
        # Check if a User with this email already exists (e.g. created during student registration)
        user = User.objects.filter(email=instance.email).first()
        if not user:
            username = instance.email
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, email=instance.email, password=instance.student_id)
                user.first_name = instance.name
                user.save()
            else:
                user = User.objects.get(username=username)
        
        # Create/sync StudentProfile
        StudentProfile.objects.get_or_create(
            user=user,
            student_obj=instance,
            defaults={
                'full_name': instance.name,
                'student_id': instance.student_id,
                'email': instance.email,
                'course_name': instance.course,
            }
        )
    else:
        # Sync updates
        try:
            profile = StudentProfile.objects.get(student_obj=instance)
            profile.full_name = instance.name
            profile.email = instance.email
            profile.course_name = instance.course
            profile.save()
            
            # Sync user
            user = profile.user
            user.email = instance.email
            user.first_name = instance.name
            user.save()
        except StudentProfile.DoesNotExist:
            user = User.objects.filter(email=instance.email).first()
            if not user:
                username = instance.email
                if not User.objects.filter(username=username).exists():
                    user = User.objects.create_user(username=username, email=instance.email, password=instance.student_id)
                    user.first_name = instance.name
                    user.save()
                else:
                    user = User.objects.get(username=username)
            StudentProfile.objects.create(
                user=user,
                student_obj=instance,
                full_name=instance.name,
                student_id=instance.student_id,
                email=instance.email,
                course_name=instance.course
            )


