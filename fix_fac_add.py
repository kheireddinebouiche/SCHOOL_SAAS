import re

file_path = 'c:/Users/kheir/Documents/saldae/SCHOOL_SAAS/templates/tenant_folder/conseil/configure-facture.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_block = """            const baseAt = q * p;
            const discountedAt = baseAt * (1 - r/100);

            const itemData = {
                id: editingIndex > -1 ? items[editingIndex].id : Date.now(),
                thematique_id: tId,
                specialite_id: null,
                description: d || getTLab(tId),
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
                addItemBtn.innerHTML = '<i class="ri-add-line fs-18"></i>'; // Reset to add icon
                addItemBtn.classList.remove('btn-warning');
                addItemBtn.classList.add('btn-primary'); // Assuming btn-primary is the default add button class
            } else {
                items.push(itemData);
            }

            renderItems();
            newThematique.value = ""; newDesignation.value=""; newLongDescription.value=""; newPrice.value="0.00"; newQty.value="1"; document.getElementById('newUnit').value="participant"; newRemise.value="0"; newRowTotal.textContent="0.00";"""

new_block = """            const finalizeAddItem = (finalTId, finalD) => {
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

                renderItems();
                // Instead of direct assignment, let's trigger change event if newThematique is a select2, though the original code just had `newThematique.value = ""`
                // Assuming it might be a normal select or a select2, we trigger change safely:
                $(newThematique).val(null).trigger('change');
                newDesignation.value=""; newLongDescription.value=""; newPrice.value="0.00"; newQty.value="1"; document.getElementById('newUnit').value="participant"; newRemise.value="0"; newRowTotal.textContent="0.00";
            };

            if (!tId && d) {
                alertify.confirm("Nouvelle thématique", "Voulez-vous enregistrer cette désignation comme une nouvelle thématique pour vos prochaines factures ?",
                    function() {
                        fetch("{% url 't_conseil:ApiCreateThematique' %}", {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': '{{ csrf_token }}',
                                'X-Requested-With': 'XMLHttpRequest'
                            },
                            body: JSON.stringify({
                                label: d,
                                description: longDesc,
                                prix: p,
                                tva: tva,
                                unite: u
                            })
                        })
                        .then(res => res.json())
                        .then(data => {
                            if (data.status === 'success') {
                                alertify.success("Thématique enregistrée avec succès.");
                                const opt = new Option(data.label, data.id);
                                opt.dataset.price = data.prix;
                                opt.dataset.tva = data.tva;
                                newThematique.add(opt);
                                // Ensure thematiques array is updated if it exists
                                if (typeof thematiques !== 'undefined') {
                                    thematiques.push({id: data.id, label: data.label, prix: data.prix, default_tva: data.tva});
                                }
                                finalizeAddItem(data.id, data.label);
                            } else {
                                alertify.error(data.message);
                                finalizeAddItem(null, d);
                            }
                        })
                        .catch(err => {
                            alertify.error("Erreur lors de la création de la thématique.");
                            finalizeAddItem(null, d);
                        });
                    },
                    function() {
                        finalizeAddItem(null, d);
                    }
                ).set('labels', {ok:'Oui, l\\'enregistrer', cancel:'Non, juste pour cette facture'});
            } else {
                finalizeAddItem(tId, d || (typeof getTLab === 'function' ? getTLab(tId) : ''));
            }"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Done")
else:
    print("Not found")

