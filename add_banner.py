import re

files = [
    r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\templates\tenant_folder\comptabilite\echeancier\details-suivie-echeancier.html',
    r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\templates\tenant_folder\comptabilite\echeancier\details-suivie-echeancier-double.html'
]

banner_html = '''
                    <!-- Notification d'avertissement procédure remboursement -->
                    <div style="display: none !important;" class="alert alert-warning d-flex align-items-center notification-banner" role="alert" id="remboursementProcedureNotification">
                        <i class="ri-error-warning-line me-3 fs-4"></i>
                        <div class="flex-grow-1">
                            <strong>Avertissement : Étudiant en procédure de remboursement.</strong>
                            <p class="mb-0 text-muted small">Ce profil est actuellement impliqué dans une procédure de remboursement.</p>
                        </div>
                    </div>
'''

def replace_banner_and_js(content):
    # Insert banner after reductionSuccessNotification
    if 'id="remboursementProcedureNotification"' not in content:
        target = r'(id=[\'\"]reductionSuccessNotification[\'\"][^>]*>.*?</div>\s*</div>)'
        content = re.sub(target, r'\1\n' + banner_html, content, flags=re.DOTALL)
    
    # Replace ShowRefundNotification
    js_target = r'function ShowRefundNotification\(has_pending_refund, has_processed_refund = false, is_appliced = false\)\{.*?\n        \}'
    
    new_js = '''function ShowRefundNotification(has_pending_refund, has_processed_refund = false, is_appliced = false){
            if((has_processed_refund && !is_appliced) || has_pending_refund){
                var el = document.getElementById('remboursementProcedureNotification');
                if (el) el.style.setProperty("display", "flex", "important");
                
                var btn1 = document.getElementById('btnNewPaiementModal');
                if (btn1) btn1.disabled = true;
                
                var btn2 = document.getElementById('btnPrintEngagement');
                if (btn2) btn2.disabled = true;
            } else {
                var el = document.getElementById('remboursementProcedureNotification');
                if (el) el.style.setProperty("display", "none", "important");
                
                var btn1 = document.getElementById('btnNewPaiementModal');
                if (btn1) btn1.disabled = false;
                
                var btn2 = document.getElementById('btnPrintEngagement');
                if (btn2) btn2.disabled = false;
            }
        }'''
    
    content = re.sub(js_target, new_js, content, flags=re.DOTALL)
    return content

for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = replace_banner_and_js(content)
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Banner added to', fpath)
