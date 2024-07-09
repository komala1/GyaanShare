#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NotesSharingProject.settings')
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


# This script is used to interact with your Django project from the command line. You can use it to run your server, make database migrations, create apps, and more.
# The script sets up the environment for Django administrative tasks by configuring the settings module.
# It attempts to import and use Django’s command-line execution function.
# If there are issues with the Django installation, it provides a helpful error message.
# When run directly, it invokes the main function to process command-line arguments and run the appropriate Django commands.