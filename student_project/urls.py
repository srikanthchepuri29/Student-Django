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
    path('logout.html', views.logout_view, name='logout'),

    # Root static assets serving (keeps existing HTML links intact without modifications)
    path('style.css', serve, {'path': 'style.css'}),
    path('student.css', serve, {'path': 'student.css'}),
    path('courses.css', serve, {'path': 'courses.css'}),
    path('teachers.css', serve, {'path': 'teachers.css'}),
    path('settings.css', serve, {'path': 'settings.css'}),
    path('login.css', serve, {'path': 'login.css'}),
    path('script.js', serve, {'path': 'script.js'}),
    path('courses.js', serve, {'path': 'courses.js'}),
    path('teachers.js', serve, {'path': 'teachers.js'}),
    path('settings.js', serve, {'path': 'settings.js'}),
    path('srikanth.png', serve, {'path': 'srikanth.png'}),

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
]
