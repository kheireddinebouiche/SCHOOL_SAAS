with open('templates/tenant_folder/exams/details_sessions_exams_plan.html', 'r', encoding='utf-8', errors='ignore') as f:
    for i, line in enumerate(f, 1):
        if 'modal' in line.lower() or '<th' in line.lower() or 'id=' in line.lower() or 'class="table' in line.lower():
            stripped = line.strip()
            if len(stripped) > 0:
                print(f'{i}: {stripped[:120]}')
