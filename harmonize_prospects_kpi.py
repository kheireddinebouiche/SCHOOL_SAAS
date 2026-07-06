import re

file_path = 'templates/tenant_folder/crm/liste-des-prospects.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_cards = """                <!-- Total Prospects -->
                <div class="col-xl col-md-6">
                    <div class="card stat-card h-100">
                        <div class="card-body p-3">
                            <div class="d-flex align-items-center justify-content-between mb-2">
                                <div class="d-flex align-items-center gap-3">
                                    <div class="stat-icon bg-primary bg-opacity-10 text-primary">
                                        <i class="ri-group-line"></i>
                                    </div>
                                    <h3 class="fw-bold mb-0"><span class="counter-value" id="totalProspects">0</span></h3>
                                </div>
                                <span class="badge bg-primary bg-opacity-10 text-primary rounded-pill">Total</span>
                            </div>
                            <p class="text-muted mb-0 small">Total Prospects</p>
                        </div>
                    </div>
                </div>

                <!-- Particuliers -->
                <div class="col-xl col-md-6">
                    <div class="card stat-card h-100">
                        <div class="card-body p-3">
                            <div class="d-flex align-items-center justify-content-between mb-2">
                                <div class="d-flex align-items-center gap-3">
                                    <div class="stat-icon bg-info bg-opacity-10 text-info">
                                        <i class="ri-user-line"></i>
                                    </div>
                                    <h3 class="fw-bold mb-0"><span class="counter-value" id="particuliersCount">0</span></h3>
                                </div>
                                <span class="badge bg-info bg-opacity-10 text-info rounded-pill">Particuliers</span>
                            </div>
                            <p class="text-muted mb-0 small">Prospects B2C</p>
                        </div>
                    </div>
                </div>

                <!-- Entreprises -->
                <div class="col-xl col-md-6">
                    <div class="card stat-card h-100">
                        <div class="card-body p-3">
                            <div class="d-flex align-items-center justify-content-between mb-2">
                                <div class="d-flex align-items-center gap-3">
                                    <div class="stat-icon bg-danger bg-opacity-10 text-danger">
                                        <i class="ri-building-line"></i>
                                    </div>
                                    <h3 class="fw-bold mb-0"><span class="counter-value" id="entreprisesCount">0</span></h3>
                                </div>
                                <span class="badge bg-danger bg-opacity-10 text-danger rounded-pill">Entreprises</span>
                            </div>
                            <p class="text-muted mb-0 small">Prospects B2B</p>
                        </div>
                    </div>
                </div>

                <!-- En Attente -->
                <div class="col-xl col-md-6">
                    <div class="card stat-card h-100">
                        <div class="card-body p-3">
                            <div class="d-flex align-items-center justify-content-between mb-2">
                                <div class="d-flex align-items-center gap-3">
                                    <div class="stat-icon bg-warning bg-opacity-10 text-warning">
                                        <i class="ri-time-line"></i>
                                    </div>
                                    <h3 class="fw-bold mb-0"><span class="counter-value" id="enAttenteCount">0</span></h3>
                                </div>
                                <span class="badge bg-warning bg-opacity-10 text-warning rounded-pill">En attente</span>
                            </div>
                            <p class="text-muted mb-0 small">À contacter</p>
                        </div>
                    </div>
                </div>

                <!-- Sans Fiche -->
                <div class="col-xl col-md-6">
                    <div class="card stat-card h-100">
                        <div class="card-body p-3">
                            <div class="d-flex align-items-center justify-content-between mb-2">
                                <div class="d-flex align-items-center gap-3">
                                    <div class="stat-icon bg-secondary bg-opacity-10 text-secondary">
                                        <i class="ri-file-warning-line"></i>
                                    </div>
                                    <h3 class="fw-bold mb-0"><span class="counter-value" id="sansVoeuxCount">0</span></h3>
                                </div>
                                <span class="badge bg-secondary bg-opacity-10 text-secondary rounded-pill">Sans fiche</span>
                            </div>
                            <p class="text-muted mb-0 small">Sans voeux</p>
                        </div>
                    </div>
                </div>"""

new_cards = """                <!-- Total Prospects -->
                <div class="col-xl col-md-6">
                    <div class="card stat-card h-100">
                        <div class="card-body p-2 d-flex align-items-center">
                            <div class="stat-icon bg-primary bg-opacity-10 text-primary me-3" style="width: 48px; height: 48px; font-size: 1.5rem; flex-shrink: 0;">
                                <i class="ri-group-line"></i>
                            </div>
                            <div>
                                <p class="text-muted mb-1 small text-uppercase fw-semibold" style="font-size: 0.75rem;">Total</p>
                                <h4 class="fw-bold mb-0"><span class="counter-value" id="totalProspects">0</span></h4>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Particuliers -->
                <div class="col-xl col-md-6">
                    <div class="card stat-card h-100">
                        <div class="card-body p-2 d-flex align-items-center">
                            <div class="stat-icon bg-info bg-opacity-10 text-info me-3" style="width: 48px; height: 48px; font-size: 1.5rem; flex-shrink: 0;">
                                <i class="ri-user-line"></i>
                            </div>
                            <div>
                                <p class="text-muted mb-1 small text-uppercase fw-semibold" style="font-size: 0.75rem;">Particuliers</p>
                                <h4 class="fw-bold mb-0"><span class="counter-value" id="particuliersCount">0</span></h4>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Entreprises -->
                <div class="col-xl col-md-6">
                    <div class="card stat-card h-100">
                        <div class="card-body p-2 d-flex align-items-center">
                            <div class="stat-icon bg-danger bg-opacity-10 text-danger me-3" style="width: 48px; height: 48px; font-size: 1.5rem; flex-shrink: 0;">
                                <i class="ri-building-line"></i>
                            </div>
                            <div>
                                <p class="text-muted mb-1 small text-uppercase fw-semibold" style="font-size: 0.75rem;">Entreprises</p>
                                <h4 class="fw-bold mb-0"><span class="counter-value" id="entreprisesCount">0</span></h4>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- En Attente -->
                <div class="col-xl col-md-6">
                    <div class="card stat-card h-100">
                        <div class="card-body p-2 d-flex align-items-center">
                            <div class="stat-icon bg-warning bg-opacity-10 text-warning me-3" style="width: 48px; height: 48px; font-size: 1.5rem; flex-shrink: 0;">
                                <i class="ri-time-line"></i>
                            </div>
                            <div>
                                <p class="text-muted mb-1 small text-uppercase fw-semibold" style="font-size: 0.75rem;">En attente</p>
                                <h4 class="fw-bold mb-0"><span class="counter-value" id="enAttenteCount">0</span></h4>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Sans Fiche -->
                <div class="col-xl col-md-6">
                    <div class="card stat-card h-100">
                        <div class="card-body p-2 d-flex align-items-center">
                            <div class="stat-icon bg-secondary bg-opacity-10 text-secondary me-3" style="width: 48px; height: 48px; font-size: 1.5rem; flex-shrink: 0;">
                                <i class="ri-file-warning-line"></i>
                            </div>
                            <div>
                                <p class="text-muted mb-1 small text-uppercase fw-semibold" style="font-size: 0.75rem;">Sans fiche</p>
                                <h4 class="fw-bold mb-0"><span class="counter-value" id="sansVoeuxCount">0</span></h4>
                            </div>
                        </div>
                    </div>
                </div>"""

if old_cards in content:
    content = content.replace(old_cards, new_cards)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("KPI layout updated successfully in liste-des-prospects.html!")
else:
    print("Could not find the exact KPI string to replace.")
