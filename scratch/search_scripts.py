with open('templates/tenant_folder/exams/details_sessions_exams_plan.html', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f, 1):
        if '<script' in line.lower():
            print(f'Line {i}: {line.strip()}')
