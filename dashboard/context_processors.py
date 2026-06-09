from .models import UserProfile

def profile_settings(request):
    if request.user.is_authenticated:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        return {'profile': profile}
    return {
        'profile': {
            'admin_name': 'Admin',
            'admin_email': 'admin@gmail.com',
            'admin_avatar': 'srikanth.png',
            'theme': 'light',
            'accent_color': '#2563eb',
            'accent_hover': '#1d4ed8',
            'notif_email': True,
            'notif_student': True,
            'notif_digest': False,
        }
    }
