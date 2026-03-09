#!/usr/bin/env python
"""
Test runner script for the dashboard CRUD tests.
Run with: python run_tests.py
"""
import os
import sys
import django

# Setup Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
django.setup()

from django.core.management import execute_from_command_line

if __name__ == '__main__':
    # Run tests with verbose output
    execute_from_command_line(['manage.py', 'test', 'apps.core.tests', '-v', '2'])
