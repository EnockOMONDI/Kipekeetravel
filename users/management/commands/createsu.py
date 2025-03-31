# File: create_superuser.py
#
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Creates a superuser.'

    def handle(self, *args, **options):
        if not User.objects.filter(username='jdaadmin').exists():
            User.objects.create_superuser(
                username='jdaadmin',
                password='jdaadminpassword'
            )
            self.stdout.write(self.style.SUCCESS('Superuser has been created.'))
        else:
            self.stdout.write(self.style.WARNING('Superuser with username "jdaadmin" already exists. Skipped.'))
