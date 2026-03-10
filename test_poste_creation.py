import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from associe_app.models import PostesBudgetaire, GlobalDepensesCategory, GlobalPaymentCategory

def check_creation():
    print("Checking PosteBudgetaire creation...")
    
    # Try to create a test poste
    try:
        poste = PostesBudgetaire.objects.create(
            label="Test Poste",
            description="Testing creation logic",
            type="depense"
        )
        print(f"Successfully created: {poste.label} (ID: {poste.id})")
        
        # Check if it's in the list
        all_postes = PostesBudgetaire.objects.all()
        print(f"Total postes: {all_postes.count()}")
        
        # Cleanup
        poste.delete()
        print("Test poste deleted.")
        
    except Exception as e:
        print(f"Error creating poste: {e}")

if __name__ == "__main__":
    check_creation()
