import re

file_path = 'c:/Users/kheir/Documents/saldae/SCHOOL_SAAS/t_conseil/urls.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add the URL pattern
new_url = "path('api/thematiques/create/', views.ApiCreateThematique, name='ApiCreateThematique'),\n    "
if 'ApiLoadThematique' in content and 'ApiCreateThematique' not in content:
    content = content.replace("path('api/thematiques/load/', views.ApiLoadThematique, name='ApiLoadThematique'),", 
                              new_url + "path('api/thematiques/load/', views.ApiLoadThematique, name='ApiLoadThematique'),")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("URL added")
else:
    print("URL not added or already exists")
