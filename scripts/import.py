import csv
import os
import sys
import django

# Set the project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the project base directory to the Python path
sys.path.append(BASE_DIR)

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fremont_app.settings')

# Initialize Django
django.setup()

from core.models import Organization, OrganizationType

with open("scripts/clubs.csv", encoding='utf-8') as f:
    reader = csv.DictReader(f)
    clubs = list(reader)

for x in clubs:
    name = x["Club"]
    obj, _ = Organization.objects.get_or_create(
        name=name, defaults=dict(type=OrganizationType.CLUB)
    )
    obj.description = x["Description"]
    obj.save()

    print(obj)
