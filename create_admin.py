#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mic_radiology.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
user, created = User.objects.get_or_create(username='admin', email='admin@micradiology.com')
user.set_password('admin123')
user.is_staff = True
user.is_superuser = True
user.is_verified = True
user.save()
print(f"✓ Superuser {'created' if created else 'updated'}: admin")
print(f"  Email: admin@micradiology.com")
print(f"  Password: admin123")
