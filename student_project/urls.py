from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.views import serve
from dashboard import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Pages
    path('', views.index_view, name='index_root'),
    path('index.html', views.index_view, name='index'),
    path('student.html', views.student_view, name='student'),
    path('courses.html', views.courses_view, name='courses'),
    path('teachers.html', views.teachers_view, name='teachers'),
    path('schedule.html', views.schedule_view, name='schedule'),
    path('reports.html', views.reports_view, name='reports'),
    path('settings.html', views.settings_view, name='settings'),
    path('login.html', views.login_view, name='login'),
    path('register.html', views.register_view, name='register'),
    path('student_register.html', views.student_register_view, name='student_register'),
    path('logout.html', views.logout_view, name='logout'),
    
    # Admin Student Portal Management Pages
    path('manage_lms.html', views.manage_lms_view, name='manage_lms'),
    path('manage_mcq.html', views.manage_mcq_view, name='manage_mcq'),
    path('manage_coding.html', views.manage_coding_view, name='manage_coding'),
    path('manage_schedule.html', views.manage_schedule_view, name='manage_schedule'),
    path('manage_assignments.html', views.manage_assignments_view, name='manage_assignments'),

    # Root static assets serving (keeps existing HTML links intact without modifications)
    path('style.css', serve, {'path': 'style.css', 'insecure': True}),
    path('student.css', serve, {'path': 'student.css', 'insecure': True}),
    path('courses.css', serve, {'path': 'courses.css', 'insecure': True}),
    path('teachers.css', serve, {'path': 'teachers.css', 'insecure': True}),
    path('settings.css', serve, {'path': 'settings.css', 'insecure': True}),
    path('login.css', serve, {'path': 'login.css', 'insecure': True}),
    path('script.js', serve, {'path': 'script.js', 'insecure': True}),
    path('sidebar.js', serve, {'path': 'sidebar.js', 'insecure': True}),
    path('courses.js', serve, {'path': 'courses.js', 'insecure': True}),
    path('teachers.js', serve, {'path': 'teachers.js', 'insecure': True}),
    path('settings.js', serve, {'path': 'settings.js', 'insecure': True}),
    path('srikanth.png', serve, {'path': 'srikanth.png', 'insecure': True}),
    path('student_portal.css', serve, {'path': 'student_portal.css', 'insecure': True}),
    path('student_portal.js', serve, {'path': 'student_portal.js', 'insecure': True}),

    # Student Portal Pages
    path('student/dashboard.html', views.student_dashboard_view, name='student_dashboard'),
    path('student/profile.html', views.student_profile_view, name='student_profile'),
    path('student/lms.html', views.student_lms_view, name='student_lms'),
    path('student/mcq.html', views.student_mcq_view, name='student_mcq'),
    path('student/coding.html', views.student_coding_view, name='student_coding'),
    path('student/schedule.html', views.student_schedule_view, name='student_schedule'),
    path('student/assignments.html', views.student_assignments_view, name='student_assignments'),

    # REST APIs
    path('api/login/', views.api_login, name='api_login'),
    path('api/register/', views.api_register, name='api_register'),
    path('api/students/', views.api_students, name='api_students'),
    path('api/students/<int:pk>/', views.api_student_detail, name='api_student_detail'),
    path('api/teachers/', views.api_teachers, name='api_teachers'),
    path('api/teachers/<int:pk>/', views.api_teacher_detail, name='api_teacher_detail'),
    path('api/courses/', views.api_courses, name='api_courses'),
    path('api/courses/<int:pk>/', views.api_course_detail, name='api_course_detail'),
    path('api/dashboard/stats/', views.api_dashboard_stats, name='api_dashboard_stats'),
    path('api/logs/', views.api_logs, name='api_logs'),
    path('api/profile/', views.api_profile, name='api_profile'),
    path('api/theme/', views.api_theme, name='api_theme'),
    path('api/notifications/', views.api_notifications, name='api_notifications'),
    path('api/change-password/', views.api_change_password, name='api_change_password'),
    path('api/backup/export/', views.api_backup_export, name='api_backup_export'),
    path('api/backup/import/', views.api_backup_import, name='api_backup_import'),
    path('api/reset/', views.api_reset, name='api_reset'),
    
    # Admin Content Management APIs
    path('api/admin/lms/', views.api_admin_lms, name='api_admin_lms'),
    path('api/admin/lms/<int:pk>/', views.api_admin_lms_detail, name='api_admin_lms_detail'),
    path('api/admin/mcq/', views.api_admin_mcq, name='api_admin_mcq'),
    path('api/admin/mcq/<int:pk>/', views.api_admin_mcq_detail, name='api_admin_mcq_detail'),
    path('api/admin/coding/', views.api_admin_coding, name='api_admin_coding'),
    path('api/admin/coding/<int:pk>/', views.api_admin_coding_detail, name='api_admin_coding_detail'),
    path('api/admin/schedule/', views.api_admin_schedule, name='api_admin_schedule'),
    path('api/admin/schedule/<int:pk>/', views.api_admin_schedule_detail, name='api_admin_schedule_detail'),
    path('api/admin/assignments/', views.api_admin_assignments, name='api_admin_assignments'),
    path('api/admin/assignments/<int:pk>/', views.api_admin_assignments_detail, name='api_admin_assignments_detail'),

    # Student Portal REST APIs
    path('api/student/profile/', views.api_student_profile, name='api_student_profile'),
    path('api/student/lms/', views.api_student_lms, name='api_student_lms'),
    path('api/student/mcq/', views.api_student_mcq, name='api_student_mcq'),
    path('api/student/coding/', views.api_student_coding, name='api_student_coding'),
    path('api/student/schedule/', views.api_student_schedule, name='api_student_schedule'),
    path('api/student/assignments/', views.api_student_assignments, name='api_student_assignments'),
    path('api/student/stats/', views.api_student_stats, name='api_student_stats'),
    path('api/student/announcements/', views.api_student_announcements, name='api_student_announcements'),
    path('api/student/register/', views.api_student_register, name='api_student_register'),
]

