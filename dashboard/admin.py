from django.contrib import admin
from .models import (
    Student, Teacher, Course, ActivityLog, UserProfile,
    Batch, StudentProfile, LearningMaterial, MCQ, MCQAttempt,
    CodingChallenge, CodingChallengeSubmission, Assignment,
    AssignmentSubmission, Announcement, StudentProgress, WeeklyScheduleOverride
)

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

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'joining_date')
    search_fields = ('name', 'course__title')
    list_filter = ('course',)

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'student_id', 'email', 'course_name', 'batch')
    search_fields = ('full_name', 'student_id', 'email', 'course_name')
    list_filter = ('course_name', 'batch')

@admin.register(LearningMaterial)
class LearningMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'material_type', 'file_type', 'course_name', 'uploaded_at')
    search_fields = ('title', 'material_type', 'course_name')
    list_filter = ('material_type', 'file_type', 'course_name')

@admin.register(MCQ)
class MCQAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'category', 'correct_option')
    search_fields = ('question_text', 'category')
    list_filter = ('category',)

@admin.register(MCQAttempt)
class MCQAttemptAdmin(admin.ModelAdmin):
    list_display = ('student', 'category', 'score', 'total_questions', 'attempted_at')
    search_fields = ('student__full_name', 'category')
    list_filter = ('category', 'attempted_at')

@admin.register(CodingChallenge)
class CodingChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'category', 'show_solution_to_students')
    search_fields = ('title', 'category')
    list_filter = ('difficulty', 'category')

@admin.register(CodingChallengeSubmission)
class CodingChallengeSubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'challenge', 'status', 'submitted_at')
    search_fields = ('student__full_name', 'challenge__title')
    list_filter = ('status', 'submitted_at')

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course_name', 'due_date', 'created_at')
    search_fields = ('title', 'course_name')
    list_filter = ('course_name', 'created_at')

@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'status', 'submitted_at')
    search_fields = ('student__full_name', 'assignment__title')
    list_filter = ('status', 'submitted_at')

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'course_name', 'created_at')
    search_fields = ('title', 'course_name', 'content')
    list_filter = ('course_name', 'created_at')

@admin.register(StudentProgress)
class StudentProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'completion_percentage', 'last_active')
    search_fields = ('student__full_name',)
    list_filter = ('completion_percentage', 'last_active')

@admin.register(WeeklyScheduleOverride)
class WeeklyScheduleOverrideAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'day_of_week', 'time_slot', 'activity_type', 'subject', 'instructor')
    search_fields = ('course_name', 'subject', 'instructor')
    list_filter = ('course_name', 'day_of_week')


