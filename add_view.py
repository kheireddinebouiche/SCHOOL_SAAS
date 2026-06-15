import json

file_path = 'c:/Users/kheir/Documents/saldae/SCHOOL_SAAS/t_conseil/views.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_view = '''
@login_required(login_url="institut_app:login")
@module_permission(allowed_modules=['conseil'])
def ApiCreateThematique(request):
    import json
    import decimal
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            label = data.get('label')
            description = data.get('description', '')
            prix = data.get('prix', 0)
            tva = data.get('tva', 19.00)
            
            try:
                prix = decimal.Decimal(str(prix))
                tva = decimal.Decimal(str(tva))
            except:
                prix = 0
                tva = 19.00
                
            thematique = Thematiques.objects.create(
                label=label,
                description=description,
                prix=prix,
                default_tva=tva
            )
            return JsonResponse({'status': 'success', 'id': thematique.id, 'label': thematique.label, 'prix': str(thematique.prix), 'tva': str(thematique.default_tva)})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
'''

# Find a good place to insert it. E.g., before ApiLoadThematique
if 'def ApiLoadThematique' in content:
    content = content.replace('def ApiLoadThematique', new_view + '\ndef ApiLoadThematique')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("View added")
else:
    print("Could not find ApiLoadThematique")
