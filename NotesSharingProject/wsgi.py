"""
WSGI config for NotesSharingProject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application




os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NotesSharingProject.settings')
application = get_wsgi_application()


# Stands for Web Server Gateway Interface. It is used to help your Django application communicate with web servers. This is the entry point for WSGI-compatible web servers to serve your project.
# Purpose: The wsgi.py file sets up the WSGI application for your Django project, allowing it to communicate with web servers that follow the WSGI standard.
# Key Components:
# Docstring: Provides a brief explanation and reference to Django documentation.
# Imports: Imports necessary modules (os and get_wsgi_application).
# Environment Variable: Sets the DJANGO_SETTINGS_MODULE to point to the project's settings module.
# WSGI Application: Creates the WSGI application callable (application) used by WSGI servers to handle request
# bridge bet web server and views file  :user send req then req go to server thwn from server to view  with help of wsgi.py