from django.contrib import admin
from .models import Student, Teacher, Course, ActivityLog, UserProfile

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name', 'email', 'course', 'status')
    search_fields = ('student_id', 'name', 'email', 'course')
    list_filter = ('status', 'course')

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher_id', 'name', 'email', 'spec', 'exp', 'status')
    search_fields = ('teacher_id', 'name', 'email', 'spec')
    list_filter = ('status', 'spec')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'title', 'teacher', 'category', 'duration', 'status')
    search_fields = ('course_id', 'title', 'teacher', 'category')
    list_filter = ('status', 'category')

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'details', 'timestamp')
    search_fields = ('action', 'details')
    list_filter = ('timestamp',)
    readonly_fields = ('timestamp',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'admin_name', 'admin_email', 'theme', 'accent_color')
    search_fields = ('admin_name', 'admin_email', 'user__username')

