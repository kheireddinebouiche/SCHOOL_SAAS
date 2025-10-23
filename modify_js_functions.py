import sys
print("Démarrage du script de modification des fonctions JS")
sys.stdout.flush()

# Read the file
try:
    with open('C:\\Users\\Bureau IT\\Documents\\SCHOOL_SAAS\\templates\\tenant_folder\\formateur\\affectation_modules.html', 'r', encoding='utf-8') as file:
        content = file.read()
    print("Fichier lu avec succès")
    sys.stdout.flush()
except Exception as e:
    print(f"Erreur lors de la lecture: {e}")
    sys.stdout.flush()
    exit(1)

# Modification de la fonction loadAvailableTrainers()
old_loadTrainers = '''      $.each(mockTrainers, function(index, trainer) {
        html += '<tr>';
        html += '<td><div class=\"form-check\"><input class=\"form-check-input module-checkbox\" type=\"checkbox\" value=\"' + trainer.id + '\" id=\"trainer_' + trainer.id + '\"></div></td>';
        html += '<td><span class=\"fw-semibold\">' + trainer.nom + '</span></td>';
        html += '<td>' + trainer.prenom + '</td>';
        html += '<td>' + trainer.email + '</td>';
        html += '</tr>';
      });'''

new_loadTrainers = '''      $.each(mockTrainers, function(index, trainer) {
        html += '<tr>';
        html += '<td><span class=\"fw-semibold\">' + trainer.nom + '</span></td>';
        html += '<td>' + trainer.prenom + '</td>';
        html += '<td>' + trainer.email + '</td>';
        html += '<td class=\"text-center\">';
        html += '<div class=\"btn-group\" role=\"group\">';
        html += '<button type=\"button\" class=\"btn btn-sm btn-success assign-trainer\" data-trainer-id=\"' + trainer.id + '\">Affecter</button>';
        html += '<button type=\"button\" class=\"btn btn-sm btn-danger remove-trainer\" data-trainer-id=\"' + trainer.id + '\" style=\"display:none;\">Supprimer</button>';
        html += '</div>';
        html += '</td>';
        html += '</tr>';
      });'''

content = content.replace(old_loadTrainers, new_loadTrainers)
print("Fonction loadAvailableTrainers modifiée")
sys.stdout.flush()

# Modification de la fonction filterTrainers()
old_filterTrainers = '''      if (filteredTrainers.length === 0) {
        html = '<tr><td colspan=\"5\" class=\"text-center text-muted py-4\">Aucun formateur trouvé</td></tr>';
      } else {
        $.each(filteredTrainers, function(index, trainer) {
          html += '<tr>';
          html += '<td><div class=\\\"form-check\\\"><input class=\\\"form-check-input module-checkbox\\\" type=\\\"checkbox\\\" value=\\\"' + trainer.id + '\\\" id=\\\"trainer_' + trainer.id + '\\\"></div></td>';
          html += '<td><span class=\\\"fw-semibold\\\">' + trainer.nom + '</span></td>';
          html += '<td>' + trainer.prenom + '</td>';
          html += '<td>' + (trainer.specialite || 'N/A') + '</td>';
          html += '<td>' + trainer.email + '</td>';
          html += '</tr>';
        });
      }'''

new_filterTrainers = '''      if (filteredTrainers.length === 0) {
        html = '<tr><td colspan=\"4\" class=\"text-center text-muted py-4\">Aucun formateur trouvé</td></tr>';
      } else {
        $.each(filteredTrainers, function(index, trainer) {
          html += '<tr>';
          html += '<td><span class=\"fw-semibold\">' + trainer.nom + '</span></td>';
          html += '<td>' + trainer.prenom + '</td>';
          html += '<td>' + (trainer.specialite || 'N/A') + '</td>';
          html += '<td>' + trainer.email + '</td>';
          html += '<td class=\"text-center\">';
          html += '<div class=\"btn-group\" role=\"group\">';
          html += '<button type=\"button\" class=\"btn btn-sm btn-success assign-trainer\" data-trainer-id=\"' + trainer.id + '\">Affecter</button>';
          html += '<button type=\"button\" class=\"btn btn-sm btn-danger remove-trainer\" data-trainer-id=\"' + trainer.id + '\" style=\"display:none;\">Supprimer</button>';
          html += '</div>';
          html += '</td>';
          html += '</tr>';
        });
      }'''

content = content.replace(old_filterTrainers, new_filterTrainers)
print("Fonction filterTrainers modifiée")
sys.stdout.flush()

# Modification du colspan dans le cas où il n'y a pas de formateurs (il devait être 5, maintenant c'est 4)
content = content.replace(
    '<tr><td colspan=\"5\" class=\"text-center text-muted py-4\">Aucun formateur trouvé</td></tr>',
    '<tr><td colspan=\"4\" class=\"text-center text-muted py-4\">Aucun formateur trouvé</td></tr>'
)

# Écrire le fichier modifié
with open('C:\\Users\\Bureau IT\\Documents\\SCHOOL_SAAS\\templates\\tenant_folder\\formateur\\affectation_modules.html', 'w', encoding='utf-8') as file:
    file.write(content)

print("Toutes les modifications effectuées avec succès")