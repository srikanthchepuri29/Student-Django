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
