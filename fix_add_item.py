import re

file_path = 'c:/Users/kheir/Documents/saldae/SCHOOL_SAAS/templates/tenant_folder/conseil/configure-devis.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_block = '''                const finalizeAddItem = (finalTId, finalD) => {
                    const baseAt = q * p;
                    const discountedAt = baseAt * (1 - r/100);

                    const itemData = {
                        id: editingIndex > -1 ? items[editingIndex].id : Date.now(),
                        thematique_id: finalTId,
                        specialite_id: null,
                        description: finalD,
                        long_description: longDesc,
                        quantity: q,
                        unit: u,
                        unitPrice: p,
                        remise_percent: r,
                        tva_percent: tva,
                        total: discountedAt
                    };

                    if(editingIndex > -1) {
                        items[editingIndex] = itemData;
                        editingIndex = -1;
                        addItemBtn.innerHTML = '<i class="ri-add-line fs-18"></i>';
                        addItemBtn.classList.remove('btn-warning');
                        addItemBtn.classList.add('btn-primary');
                    } else {
                        items.push(itemData);
                    }

                    setDirty(true);
                    renderItems();'''

# It means the previous replace partially worked up to the powershell error?
# Wait, let's just check if it was replaced or not.
