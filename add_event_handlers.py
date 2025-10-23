import sys
print("Démarrage du script d'ajout des gestionnaires d'événements")
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

# Trouver la fin du script pour ajouter les gestionnaires d'événements
# Cherchons une fin de fonction appropriée avant la fin du script
end_script_idx = content.rfind('$(document).ready(function () {')
if end_script_idx != -1:
    # Trouvons où se termine le script
    end_ready_idx = content.rfind('});', end_script_idx)
    if end_ready_idx != -1:
        # Trouver le bon endroit pour insérer les gestionnaires
        # Nous voulons le placer dans la fonction principale
        # Cherchons une fin de fonction avant le }); final
        last_function_end = content.rfind('});', 0, end_ready_idx)
        if last_function_end != -1:
            # Trouvons la fin de cette fonction
            next_brace = content.find('}', last_function_end)
            if next_brace != -1:
                # Insérons le code après cette fonction
                insert_pos = content.find('\n', next_brace) + 1
                if insert_pos > 0:
                    # Code à insérer
                    event_handlers = '''

    // Gestionnaire pour le bouton Affecter
    $(document).on('click', '.assign-trainer', function() {
      var trainerId = $(this).data('trainer-id');
      var row = $(this).closest('tr');
      
      // Changer le bouton Affecter en Supprimer
      $(this).hide();
      row.find('.remove-trainer').show();
      
      // Ajouter le formateur à la liste des affectations
      // (logique à implémenter selon vos besoins)
      console.log('Formateur ID ' + trainerId + ' affecté');
    });
    
    // Gestionnaire pour le bouton Supprimer
    $(document).on('click', '.remove-trainer', function() {
      var trainerId = $(this).data('trainer-id');
      var row = $(this).closest('tr');
      
      // Changer le bouton Supprimer en Affecter
      $(this).hide();
      row.find('.assign-trainer').show();
      
      // Retirer le formateur de la liste des affectations
      // (logique à implémenter selon vos besoins)
      console.log('Formateur ID ' + trainerId + ' supprimé');
    });
'''
                    new_content = content[:insert_pos] + event_handlers + content[insert_pos:]
                    
                    # Écrire le fichier modifié
                    with open('C:\\Users\\Bureau IT\\Documents\\SCHOOL_SAAS\\templates\\tenant_folder\\formateur\\affectation_modules.html', 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    
                    print("Gestionnaires d'événements ajoutés avec succès")
                else:
                    print("Impossible de trouver un endroit approprié pour l'insertion")
            else:
                print("Impossible de trouver la structure appropriée")
        else:
            print("Impossible de trouver une fin de fonction appropriée")
    else:
        print("Impossible de trouver la fin du document ready")
else:
    print("Impossible de trouver le document ready")