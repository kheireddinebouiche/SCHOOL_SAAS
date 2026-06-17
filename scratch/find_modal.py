content = open('templates/tenant_folder/conseil/nouveau-devis.html', encoding='utf-8', errors='ignore').read()
idx1 = content.find('id="quickProspectForm"')
if idx1 != -1:
    idx2 = content.rfind('<div class="modal', 0, idx1)
    print("MODAL START:", content[max(0, idx2):idx1+500])

    idx3 = content.find('data-bs-target', content.find('prospect', 0, idx2) - 100)
    print("TRIGGER TARGET?:", content[max(0, idx3-100):idx3+100])
