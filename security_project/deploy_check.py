#!/usr/bin/env python
import os
import sys
import django
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

def check_deployment():
    print("Running deployment checks...")
    
    
    from django.conf import settings
    assert not settings.DEBUG, "DEBUG should be False in production"
    assert settings.SECRET_KEY != "your-secret-key-here", "Change the default SECRET_KEY"
    
   
    from django.db import connection
    try:
        connection.ensure_connection()
        print(" Database connection successful")
    except Exception as e:
        print(f" Database connection failed: {e}")
        return False
    
  
    try:
        from your_project.celery import app
        app.control.inspect().ping()
        print(" Celery connection successful")
    except Exception as e:
        print(f" Celery connection failed: {e}")
        return False
    
    
    from django.test import Client
    client = Client()
    response = client.get('/swagger/')
    assert response.status_code in [200, 302], f"Swagger returned {response.status_code}"
    print(" Swagger endpoint accessible")
    
    print("All deployment checks passed!")
    return True

if __name__ == "__main__":
    if check_deployment():
        sys.exit(0)
    else:
        sys.exit(1)