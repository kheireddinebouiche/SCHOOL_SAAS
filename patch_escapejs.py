import re

file_path = r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\templates\saas_admin_app\saas_tenant_data_explorer.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix prospect modal
content = content.replace(
    "onclick=\"openEditProspectModal('{{ p.id }}', '{{ p.nom }} {{ p.prenom }}', '{{ p.etat }}', '{{ p.statut }}')\"",
    "onclick=\"openEditProspectModal('{{ p.id }}', '{{ p.nom|escapejs }} {{ p.prenom|escapejs }}', '{{ p.etat|escapejs }}', '{{ p.statut|escapejs }}')\""
)

# Fix reset prospect
content = content.replace(
    "onclick=\"confirmResetProspect('{{ p.id }}', '{{ p.nom }} {{ p.prenom }}')\"",
    "onclick=\"confirmResetProspect('{{ p.id }}', '{{ p.nom|escapejs }} {{ p.prenom|escapejs }}')\""
)

# Fix voeu modal standard
content = content.replace(
    "onclick=\"openEditVoeuModal('{{ v.id }}', 'standard', '{{ v.specialite.id }}', '{{ v.prospect.nom }} {{ v.prospect.prenom }}', '{{ v.promo.id }}', '{{ v.is_confirmed|yesno:'true,false' }}')\"",
    "onclick=\"openEditVoeuModal('{{ v.id }}', 'standard', '{{ v.specialite.id }}', '{{ v.prospect.nom|escapejs }} {{ v.prospect.prenom|escapejs }}', '{{ v.promo.id }}', '{{ v.is_confirmed|yesno:'true,false' }}')\""
)

# Fix voeu modal double
content = content.replace(
    "onclick=\"openEditVoeuModal('{{ v.id }}', 'double', '{{ v.specialite.id }}', '{{ v.prospect.nom }} {{ v.prospect.prenom }}', '{{ v.promo.id }}', '{{ v.is_confirmed|yesno:'true,false' }}')\"",
    "onclick=\"openEditVoeuModal('{{ v.id }}', 'double', '{{ v.specialite.id }}', '{{ v.prospect.nom|escapejs }} {{ v.prospect.prenom|escapejs }}', '{{ v.promo.id }}', '{{ v.is_confirmed|yesno:'true,false' }}')\""
)

# Fix due paiement modal
content = content.replace(
    "onclick=\"openEditDuePaiementModal('{{ dp.id }}', '{{ dp.label }}', '{{ dp.montant_due }}', '{{ dp.montant_restant }}', '{{ dp.date_echeance|date:'Y-m-d' }}')\"",
    "onclick=\"openEditDuePaiementModal('{{ dp.id }}', '{{ dp.label|escapejs }}', '{{ dp.montant_due }}', '{{ dp.montant_restant }}', '{{ dp.date_echeance|date:'Y-m-d' }}')\""
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Added |escapejs to all inline onclick variables to prevent JS syntax errors.")
