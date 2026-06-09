#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_project.settings')
    
    # Auto-open browser when running development server
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        port = '8000'
        for arg in sys.argv[2:]:
            if ':' in arg:
                port = arg.split(':')[-1]
            elif arg.isdigit():
                port = arg
                
        import webbrowser
        import threading
        import time
        
        def open_browser():
            time.sleep(1.5)
            # Check if this is the reloader child process or if reload is disabled
            if os.environ.get('RUN_MAIN') == 'true' or '--noreload' in sys.argv:
                webbrowser.open(f'http://127.0.0.1:{port}/')
                
        threading.Thread(target=open_browser, daemon=True).start()

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
