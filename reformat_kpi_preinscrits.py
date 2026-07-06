import re

file_path = 'templates/tenant_folder/crm/preinscrits/liste-des-preinscrits.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_cards = """        <!-- Total -->
        <div class="col-xl-3 col-md-6">
            <div class="card stat-card h-100">
                <div class="card-body p-2">
                    <div class="d-flex align-items-center justify-content-between mb-1">
                        <div class="d-flex align-items-center gap-2">
                            <div class="stat-icon bg-primary bg-opacity-10 text-primary">
                                <i class="ri-group-line"></i>
                            </div>
                            <h4 class="fw-bold mb-0"><span class="counter-value" id="totalCount">0</span></h4>
                        </div>
                        <span class="badge bg-primary bg-opacity-10 text-primary rounded-pill">Total</span>
                    </div>
                    <p class="text-muted mb-0 small" style="font-size: 0.75rem;">Total Préinscrits</p>
                </div>
            </div>
        </div>

        <!-- Instance -->
        <div class="col-xl-3 col-md-6">
            <div class="card stat-card h-100">
                <div class="card-body p-2">
                    <div class="d-flex align-items-center justify-content-between mb-1">
                        <div class="d-flex align-items-center gap-2">
                            <div class="stat-icon bg-info bg-opacity-10 text-info">
                                <i class="ri-user-line"></i>
                            </div>
                            <h4 class="fw-bold mb-0"><span class="counter-value" id="instanceCount">0</span></h4>
                        </div>
                        <span class="badge bg-info bg-opacity-10 text-info rounded-pill">Instance</span>
                    </div>
                    <p class="text-muted mb-0 small" style="font-size: 0.75rem;">En cours de traitement</p>
                </div>
            </div>
        </div>

        <!-- Préinscrit -->
        <div class="col-xl-3 col-md-6">
            <div class="card stat-card h-100">
                <div class="card-body p-2">
                    <div class="d-flex align-items-center justify-content-between mb-1">
                        <div class="d-flex align-items-center gap-2">
                            <div class="stat-icon bg-warning bg-opacity-10 text-warning">
                                <i class="ri-time-line"></i>
                            </div>
                            <h4 class="fw-bold mb-0"><span class="counter-value" id="preinscritCount">0</span></h4>
                        </div>
                        <span class="badge bg-warning bg-opacity-10 text-warning rounded-pill">Préinscrit</span>
                    </div>
                    <p class="text-muted mb-0 small" style="font-size: 0.75rem;">Dossiers acceptés</p>
                </div>
            </div>
        </div>

        <!-- Converti -->
        <div class="col-xl-3 col-md-6">
            <div class="card stat-card h-100">
                <div class="card-body p-2">
                    <div class="d-flex align-items-center justify-content-between mb-1">
                        <div class="d-flex align-items-center gap-2">
                            <div class="stat-icon bg-success bg-opacity-10 text-success">
                                <i class="ri-checkbox-circle-line"></i>
                            </div>
                            <h4 class="fw-bold mb-0"><span class="counter-value" id="convertiCount">0</span></h4>
                        </div>
                        <span class="badge bg-success bg-opacity-10 text-success rounded-pill">Converti</span>
                    </div>
                    <p class="text-muted mb-0 small" style="font-size: 0.75rem;">Inscriptions validées</p>
                </div>
            </div>
        </div>"""

new_cards = """        <!-- Total -->
        <div class="col-xl-3 col-md-6">
            <div class="card stat-card h-100">
                <div class="card-body p-2 d-flex align-items-center">
                    <div class="stat-icon bg-primary bg-opacity-10 text-primary me-3" style="width: 48px; height: 48px; font-size: 1.5rem; flex-shrink: 0;">
                        <i class="ri-group-line"></i>
                    </div>
                    <div>
                        <p class="text-muted mb-1 small text-uppercase fw-semibold" style="font-size: 0.75rem;">Total Préinscrits</p>
                        <h4 class="fw-bold mb-0"><span class="counter-value" id="totalCount">0</span></h4>
                    </div>
                </div>
            </div>
        </div>

        <!-- Instance -->
        <div class="col-xl-3 col-md-6">
            <div class="card stat-card h-100">
                <div class="card-body p-2 d-flex align-items-center">
                    <div class="stat-icon bg-info bg-opacity-10 text-info me-3" style="width: 48px; height: 48px; font-size: 1.5rem; flex-shrink: 0;">
                        <i class="ri-user-line"></i>
                    </div>
                    <div>
                        <p class="text-muted mb-1 small text-uppercase fw-semibold" style="font-size: 0.75rem;">Instance</p>
                        <h4 class="fw-bold mb-0"><span class="counter-value" id="instanceCount">0</span></h4>
                    </div>
                </div>
            </div>
        </div>

        <!-- Préinscrit -->
        <div class="col-xl-3 col-md-6">
            <div class="card stat-card h-100">
                <div class="card-body p-2 d-flex align-items-center">
                    <div class="stat-icon bg-warning bg-opacity-10 text-warning me-3" style="width: 48px; height: 48px; font-size: 1.5rem; flex-shrink: 0;">
                        <i class="ri-time-line"></i>
                    </div>
                    <div>
                        <p class="text-muted mb-1 small text-uppercase fw-semibold" style="font-size: 0.75rem;">Préinscrit</p>
                        <h4 class="fw-bold mb-0"><span class="counter-value" id="preinscritCount">0</span></h4>
                    </div>
                </div>
            </div>
        </div>

        <!-- Converti -->
        <div class="col-xl-3 col-md-6">
            <div class="card stat-card h-100">
                <div class="card-body p-2 d-flex align-items-center">
                    <div class="stat-icon bg-success bg-opacity-10 text-success me-3" style="width: 48px; height: 48px; font-size: 1.5rem; flex-shrink: 0;">
                        <i class="ri-checkbox-circle-line"></i>
                    </div>
                    <div>
                        <p class="text-muted mb-1 small text-uppercase fw-semibold" style="font-size: 0.75rem;">Converti</p>
                        <h4 class="fw-bold mb-0"><span class="counter-value" id="convertiCount">0</span></h4>
                    </div>
                </div>
            </div>
        </div>"""

if old_cards in content:
    content = content.replace(old_cards, new_cards)
    
    # Also fix stat-icon size css if it's there
    content = content.replace('''  .stat-icon {
    width: 56px;
    height: 56px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 1rem;
    font-size: 1.75rem;
    transition: all 0.4s ease;
  }''', '''  .stat-icon {
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 1rem;
    font-size: 1.5rem;
    transition: all 0.4s ease;
  }''')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("KPI layout updated successfully!")
else:
    print("Could not find the exact KPI string to replace.")
