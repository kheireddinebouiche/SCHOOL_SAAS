import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from associe_app.utils import sync_global_categories

def test_sync():
    print("Testing sync_global_categories()...")
    try:
        sync_global_categories()
        print("Success without exceptions!")
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_sync()
