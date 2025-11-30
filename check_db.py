import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mainsection.settings')
django.setup()

try:
    from car1.models import ContactMessage
    count = ContactMessage.objects.count()
    with open('db_status.txt', 'w') as f:
        f.write(f"Success: {count} messages")
except Exception as e:
    with open('db_status.txt', 'w') as f:
        f.write(f"Error: {e}")
