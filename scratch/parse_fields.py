import re

content = open('templates/tenant_folder/crm/preinscrits/details-preinscrit.html', encoding='utf-8').read()
start = content.find('id="additionalInfoModal"')
end = content.find('id="addReminderModal"', start)
if end == -1: end = start + 50000
modal = content[start:end]

inputs = re.findall(r'<input[^>]+id="([^"]+)"', modal)
selects = re.findall(r'<select[^>]+id="([^"]+)"', modal)
textareas = re.findall(r'<textarea[^>]+id="([^"]+)"', modal)

print("Inputs:", inputs)
print("Selects:", selects)
print("Textareas:", textareas)
