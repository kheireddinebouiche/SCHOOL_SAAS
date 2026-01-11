import os
import django
import sys

# Add project root to path
sys.path.append(os.getcwd())

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school.settings")
django.setup()

from django.db import connection
cursor = connection.cursor()
cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'bejaia'")
tables = [row[0] for row in cursor.fetchall()]
print("Tables in bejaia schema matching 'app_':")
for t in tables:
    if t.startswith('app_'):
        print(t)
