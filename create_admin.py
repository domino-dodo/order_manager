import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'order_manager.settings')
django.setup()

from django.contrib.auth.models import User

username = "john"
password = "rootadmin"
email = ""

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print("Superuser created")
else:
    print("Superuser already exists")