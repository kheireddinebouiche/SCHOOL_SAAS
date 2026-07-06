import re

file_path = 'templates/tenant_folder/crm/preinscrits/prospects_incomplets.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_cards = """      <div class="row g-3 mb-3">
        <div class="col-md-6 col-xl-3">
          <div class="card stat-card h-100">
            <div class="card-body p-2">
              <div class="d-flex align-items-center justify-content-between mb-2">
                <div class="stat-icon bg-warning bg-opacity-10 text-warning">
                  <i class="ri-folder-warning-line"></i>
                </div>
                <span class="badge bg-warning bg-opacity-10 text-warning rounded-pill">Total</span>
              </div>
              <h4 class="fw-bold mb-0">{{ page_obj.paginator.count }}</h4>
              <p class="text-muted mb-0 small">Dossiers Incomplets</p>
            </div>
          </div>
        </div>
        
        <div class="col-md-6 col-xl-3">
          <div class="card stat-card h-100">
            <div class="card-body p-2">
              <div class="d-flex align-items-center justify-content-between mb-2">
                <div class="stat-icon bg-primary bg-opacity-10 text-primary">
                  <i class="ri-group-line"></i>
                </div>
                <span class="badge bg-primary bg-opacity-10 text-primary rounded-pill">Particuliers</span>
              </div>
              <h4 class="fw-bold mb-0">
                {% with individual_count=page_obj.paginator.count %}
                  {{ individual_count }}
                {% endwith %}
              </h4>
              <p class="text-muted mb-0 small">Prospects B2C</p>
            </div>
          </div>
        </div>
        
        <div class="col-md-6 col-xl-3">
          <div class="card stat-card h-100">
            <div class="card-body p-2">
              <div class="d-flex align-items-center justify-content-between mb-2">
                <div class="stat-icon bg-danger bg-opacity-10 text-danger">
                  <i class="ri-file-close-line"></i>
                </div>
                <span class="badge bg-danger bg-opacity-10 text-danger rounded-pill">Urgent</span>
              </div>
              <h4 class="fw-bold mb-0">3</h4>
              <p class="text-muted mb-0 small">Urgent à traiter</p>
            </div>
          </div>
        </div>
        
        <div class="col-md-6 col-xl-3">
          <div class="card stat-card h-100">
            <div class="card-body p-2">
              <div class="d-flex align-items-center justify-content-between mb-2">
                <div class="stat-icon bg-success bg-opacity-10 text-success">
                  <i class="ri-time-line"></i>
                </div>
                <span class="badge bg-success bg-opacity-10 text-success rounded-pill">Appels</span>
              </div>
              <h4 class="fw-bold mb-0">7</h4>
              <p class="text-muted mb-0 small">À rappeler</p>
            </div>
          </div>
        </div>
      </div>"""

new_cards = """      <div class="row g-3 mb-3">
        <div class="col-md-6 col-xl-3">
          <div class="card stat-card h-100">
            <div class="card-body p-3 d-flex align-items-center">
                <div class="stat-icon bg-warning bg-opacity-10 text-warning me-3" style="width: 48px; height: 48px; font-size: 1.5rem; flex-shrink: 0;">
                  <i class="ri-folder-warning-line"></i>
                </div>
                <div>
                  <p class="text-muted mb-1 small text-uppercase fw-semibold" style="font-size: 0.75rem;">Total</p>
                  <h4 class="fw-bold mb-0">{{ page_obj.paginator.count }}</h4>
                </div>
            </div>
          </div>
        </div>
        
        <div class="col-md-6 col-xl-3">
          <div class="card stat-card h-100">
            <div class="card-body p-3 d-flex align-items-center">
                <div class="stat-icon bg-primary bg-opacity-10 text-primary me-3" style="width: 48px; height: 48px; font-size: 1.5rem; flex-shrink: 0;">
                  <i class="ri-group-line"></i>
                </div>
                <div>
                  <p class="text-muted mb-1 small text-uppercase fw-semibold" style="font-size: 0.75rem;">Particuliers</p>
                  <h4 class="fw-bold mb-0">
                    {% with individual_count=page_obj.paginator.count %}
                      {{ individual_count }}
                    {% endwith %}
                  </h4>
                </div>
            </div>
          </div>
        </div>
        
        <div class="col-md-6 col-xl-3">
          <div class="card stat-card h-100">
            <div class="card-body p-3 d-flex align-items-center">
                <div class="stat-icon bg-danger bg-opacity-10 text-danger me-3" style="width: 48px; height: 48px; font-size: 1.5rem; flex-shrink: 0;">
                  <i class="ri-file-close-line"></i>
                </div>
                <div>
                  <p class="text-muted mb-1 small text-uppercase fw-semibold" style="font-size: 0.75rem;">Urgent</p>
                  <h4 class="fw-bold mb-0">3</h4>
                </div>
            </div>
          </div>
        </div>
        
        <div class="col-md-6 col-xl-3">
          <div class="card stat-card h-100">
            <div class="card-body p-3 d-flex align-items-center">
                <div class="stat-icon bg-success bg-opacity-10 text-success me-3" style="width: 48px; height: 48px; font-size: 1.5rem; flex-shrink: 0;">
                  <i class="ri-time-line"></i>
                </div>
                <div>
                  <p class="text-muted mb-1 small text-uppercase fw-semibold" style="font-size: 0.75rem;">À rappeler</p>
                  <h4 class="fw-bold mb-0">7</h4>
                </div>
            </div>
          </div>
        </div>
      </div>"""

if old_cards in content:
    content = content.replace(old_cards, new_cards)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("KPI layout updated successfully!")
else:
    print("Could not find the exact KPI string to replace.")
