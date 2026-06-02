import re

path_std = r"c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\templates\tenant_folder\student\profile_etudiant.html"
path_double = r"c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\templates\tenant_folder\student\profile_etudiant_double.html"

with open(path_std, "r", encoding="utf-8") as f:
    std_content = f.read()

with open(path_double, "r", encoding="utf-8") as f:
    dbl_content = f.read()

# 1. Replace <style> block
style_pattern = re.compile(r'<style>.*?</style>', re.DOTALL)
std_style = style_pattern.search(std_content).group(0)
dbl_content = style_pattern.sub(std_style, dbl_content)

# 2. Replace Profile Header
# the header in double starts with <div class="card shadow border-0 rounded-3">
# and ends right before <div class="card-body p-4">
header_pattern = re.compile(r'<div class="card shadow border-0 rounded-3">.*?<div class="card-body p-4">', re.DOTALL)
new_header = """<div class="card mb-4 border-0">
                        <div class="profile-header">
                            <div class="d-flex justify-content-between align-items-start position-relative" style="z-index: 10;">
                                <div>
                                    <span class="header-badge mb-2 d-inline-block">
                                        <i class="ri-book-open-line me-1"></i> {{ specialite_double }}
                                    </span>
                                </div>
                                <div class="d-flex gap-2">
                                    <button class="btn btn-light btn-sm text-primary fw-medium shadow-none py-1 px-3" data-bs-toggle="modal" data-bs-target="#editStudentModal">
                                        <i class="ri-edit-line me-1"></i> Modifier
                                    </button>
                                </div>
                            </div>
                            
                            <div class="d-flex align-items-end mt-3 position-relative z-2">
                                <div class="profile-avatar-wrapper me-4">
                                    <input type="file" id="photoInput" class="d-none" accept="image/*">
                                    <div class="profile-avatar position-relative overflow-hidden">
                                        {% if etudiant.photo %}
                                            <img src="{{ etudiant.photo.url }}" alt="Photo" class="w-100 h-100 object-fit-cover rounded-circle">
                                        {% else %}
                                            <i class="ri-user-line"></i>
                                        {% endif %}
                                    </div>
                                </div>
                                <div class="mb-2">
                                    <h2 class="text-white fw-bold mb-1">{{ etudiant.nom }} {{ etudiant.prenom }}</h2>
                                    <div class="d-flex align-items-center gap-3 text-white-50">
                                        <span><i class="ri-barcode-line me-1"></i> ID: {{ etudiant.matricule_interne }}</span>
                                        <span><i class="ri-mail-line me-1"></i> {{ etudiant.email }}</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="card-body p-4 pt-0">"""
dbl_content = header_pattern.sub(new_header, dbl_content, count=1)

# 3. Replace Tabs Navigation
tabs_pattern = re.compile(r'<!-- Tabs Navigation -->.*?</ul>', re.DOTALL)
new_tabs = """<!-- Tabs Navigation -->
                            <ul class="nav nav-tabs-custom mt-4 d-flex justify-content-between" id="profileTabs" role="tablist">
                                <li class="nav-item" role="presentation">
                                    <button class="nav-link active" id="info-sup-tab" data-bs-toggle="tab" data-bs-target="#info-sup" type="button" role="tab" aria-selected="true" aria-controls="info-sup">
                                        <i class="ri-user-smile-line me-2"></i>Personnel
                                    </button>
                                </li>
                                <li class="nav-item" role="presentation">
                                    <button class="nav-link" id="parents-tab" data-bs-toggle="tab" data-bs-target="#parents" type="button" role="tab" aria-selected="false" aria-controls="parents">
                                        <i class="ri-parent-line me-2"></i>Parents
                                    </button>
                                </li>
                                <li class="nav-item" role="presentation">
                                    <button class="nav-link" id="academique-tab" data-bs-toggle="tab" data-bs-target="#academique" type="button" role="tab" aria-selected="false" aria-controls="academique">
                                        <i class="ri-graduation-cap-line me-2"></i>Académique
                                    </button>
                                </li>
                                <li class="nav-item" role="presentation">
                                    <button class="nav-link" id="paiements-tab" data-bs-toggle="tab" data-bs-target="#paiements" type="button" role="tab" aria-selected="false" aria-controls="paiements">
                                        <i class="ri-bank-card-line me-2"></i>Paiements
                                    </button>
                                </li>
                                <li class="nav-item" role="presentation">
                                    <button class="nav-link" id="remises-tab" data-bs-toggle="tab" data-bs-target="#remises" type="button" role="tab" aria-selected="false" aria-controls="remises">
                                        <i class="ri-percent-line me-2"></i>Remises
                                    </button>
                                </li>
                                <li class="nav-item" role="presentation">
                                    <button class="nav-link" id="documents-tab" data-bs-toggle="tab" data-bs-target="#documents" type="button" role="tab" aria-selected="false" aria-controls="documents">
                                        <i class="ri-file-text-line me-2"></i>Documents
                                    </button>
                                </li>
                                <li class="nav-item" role="presentation">
                                    <button class="nav-link" id="echeancier-tab" data-bs-toggle="tab" data-bs-target="#echeancier" type="button" role="tab" aria-selected="false" aria-controls="echeancier">
                                        <i class="ri-calendar-check-line me-2"></i>Échéancier
                                    </button>
                                </li>
                            </ul>"""
dbl_content = tabs_pattern.sub(new_tabs, dbl_content, count=1)

# 4. Replace stats cards in Paiements tab
# Find the start of the cards row
cards_pattern = re.compile(r'<div class="row">\s*<div class="col-lg-4">\s*<div class="card bg-primary text-white border-0">.*?</div>\s*</div>\s*</div>\s*</div>', re.DOTALL)
new_cards = """<div class="row g-4 mb-4">
                                        <div class="col-lg-4">
                                            <div class="stat-card primary h-100 p-4">
                                                <div class="card-body p-0">
                                                    <div class="d-flex flex-column justify-content-between h-100">
                                                        <div class="mb-4">
                                                            <p class="text-white-50 mb-1 font-size-14 text-uppercase fw-semibold">Total à Payer</p>
                                                            <h3 class="text-white mb-0 amount-display"><span class="montant">{{total_a_paye}}</span> <small class="fs-6 opacity-75">DZA</small></h3>
                                                        </div>
                                                        <i class="ri-bank-card-line icon-watermark"></i>
                                                        <div class="progress bg-white bg-opacity-25" style="height: 4px;">
                                                            <div class="progress-bar bg-white" role="progressbar" style="width: 100%"></div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="col-lg-4">
                                            <div class="stat-card success h-100 p-4">
                                                <div class="card-body p-0">
                                                    <div class="d-flex flex-column justify-content-between h-100">
                                                        <div class="mb-4">
                                                            <p class="text-white-50 mb-1 font-size-14 text-uppercase fw-semibold">Montant Payé</p>
                                                            <h3 class="text-white mb-0 amount-display"><span class="montant">{{montant_paye}}</span> <small class="fs-6 opacity-75">DZA</small></h3>
                                                        </div>
                                                        <i class="ri-check-double-line icon-watermark"></i>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="col-lg-4">
                                            <div class="stat-card warning h-100 p-4">
                                                <div class="card-body p-0">
                                                    <div class="d-flex flex-column justify-content-between h-100">
                                                        <div class="mb-4">
                                                            <p class="text-white-50 mb-1 font-size-14 text-uppercase fw-semibold">Reste à Payer</p>
                                                            <h3 class="text-white mb-0 amount-display"><span class="montant">{{montant_due}}</span> <small class="fs-6 opacity-75">DZA</small></h3>
                                                        </div>
                                                        <i class="ri-wallet-3-line icon-watermark"></i>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>"""
dbl_content = cards_pattern.sub(new_cards, dbl_content, count=1)

# 5. Table styles modernization
dbl_content = dbl_content.replace('table table-hover align-middle mb-0', 'table table-modern mb-0')
dbl_content = dbl_content.replace('table table-hover align-middle border-0 mb-0', 'table table-modern mb-0')

with open(path_double, "w", encoding="utf-8") as f:
    f.write(dbl_content)

print("Modification done")
