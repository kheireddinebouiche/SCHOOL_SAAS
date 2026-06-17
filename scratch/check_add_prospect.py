import re

content = open('templates/tenant_folder/conseil/pipeline.html', encoding='utf-8', errors='ignore').read()
# Find button triggers for add prospect
matches = re.findall(r'<button[^>]*data-bs-target=\"([^\"]+)\"[^>]*>([^<]+)</button>', content)
print("Buttons targeting modals in pipeline:")
for m in matches:
    print(m)

# Let's also check include tags
print("\nIncludes in pipeline:")
for inc in re.findall(r'{%\s*include\s*[\'\"]([^\'\"]+)[\'\"]\s*%}', content):
    print(inc)

content_devis = open('templates/tenant_folder/conseil/nouveau-devis.html', encoding='utf-8', errors='ignore').read()
# Find button triggers for add prospect
matches_devis = re.findall(r'<button[^>]*data-bs-target=\"([^\"]+)\"[^>]*>([^<]+)</button>', content_devis)
print("\nButtons targeting modals in devis:")
for m in matches_devis:
    print(m)

# Let's also check include tags in devis
print("\nIncludes in devis:")
for inc in re.findall(r'{%\s*include\s*[\'\"]([^\'\"]+)[\'\"]\s*%}', content_devis):
    print(inc)

