#!/usr/bin/env python

from django.contrib.auth.models import User

if User.objects.count() == 0:
    admin = User.objects.create_user(
        'clay',
        'c@zapperapp.com',
        'Cfa9nTV84pRG32m7Hg647v8qu4fy7RG4AEcZ837PPk2d838kpB'
    )
    admin.set_password('admin')
    admin.is_superuser = True
    admin.is_staff = True
    admin.save()
