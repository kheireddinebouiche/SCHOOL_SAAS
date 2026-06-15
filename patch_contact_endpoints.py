import re

file_path = 't_conseil/f_views/prospects.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_endpoints = """
@login_required(login_url="institut_app:login")
@module_permission_required('con', 'edit')
def ApiEditContactEntreprise(request):
    if request.method == "POST":
        contact_id = request.POST.get('contact_id')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        poste = request.POST.get('poste')
        
        if not nom and not prenom:
            return JsonResponse({'status': 'error', 'message': "Le nom ou le prénom est obligatoire."}, status=400)
            
        try:
            from t_crm.models import ContactEntreprise
            contact = ContactEntreprise.objects.get(id=contact_id)
            contact.nom = nom
            contact.prenom = prenom
            contact.telephone = telephone
            contact.email = email
            contact.poste = poste
            contact.save()
            return JsonResponse({'status': 'success', 'message': 'Contact modifié avec succès.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Erreur lors de la modification : {str(e)}'}, status=500)
            
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)

@login_required(login_url="institut_app:login")
@module_permission_required('con', 'delete')
def ApiDeleteContactEntreprise(request):
    if request.method == "POST":
        contact_id = request.POST.get('contact_id')
        try:
            from t_crm.models import ContactEntreprise
            contact = ContactEntreprise.objects.get(id=contact_id)
            if contact.is_primary:
                return JsonResponse({'status': 'error', 'message': "Le contact principal ne peut pas être supprimé directement."}, status=400)
            contact.delete()
            return JsonResponse({'status': 'success', 'message': 'Contact supprimé avec succès.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Erreur lors de la suppression : {str(e)}'}, status=500)
            
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)

"""

# Append it at the end of the file
if "ApiEditContactEntreprise" not in content:
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(new_endpoints)
    print("Endpoints added.")
else:
    print("Endpoints already exist.")
