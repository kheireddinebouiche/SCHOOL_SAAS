import os
import re

files_to_update = [
    r"templates/tenant_folder/exams/liste-session.html",
    r"templates/tenant_folder/exams/exams_results.html",
    r"templates/tenant_folder/exams/builltins/liste.html"
]

css_block = """<style>
    /* Premium Glass-Card Styles */
    :root {
        --glass-bg: rgba(255, 255, 255, 0.85);
        --glass-border: rgba(255, 255, 255, 0.4);
        --glass-shadow: 0 8px 32px rgba(31, 38, 135, 0.07);
        --premium-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
    }
    .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid var(--glass-border);
        box-shadow: var(--glass-shadow);
        border-radius: 16px;
    }
    .bg-light { background-color: #f4f7f9 !important; }
    .icon-box {
        width: 48px;
        height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 12px;
        font-size: 1.5rem;
    }
    .stat-card {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        box-shadow: var(--premium-shadow);
        border-radius: 14px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.05);
    }
    .filter-bar {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        box-shadow: var(--premium-shadow);
        border-radius: 12px;
    }
    .table thead th {
        background-color: #f8f9fa;
        color: #495057;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 0.025em;
        padding: 1rem;
        border-bottom: 1px solid #eef0f7;
    }
    .table tbody td {
        padding: 1rem;
        border-bottom: 1px solid #f3f3f3;
        color: #495057;
    }
    .btn-rounded { border-radius: 10px; }
    .btn-pill { border-radius: 50px; }
    .group-card { background: var(--glass-bg); border: 1px solid var(--glass-border); border-radius: 16px; transition: all 0.3s ease; }
    .group-card:hover { transform: translateY(-8px); box-shadow: 0 15px 35px rgba(0,0,0,0.1); }
</style>"""

for f in files_to_update:
    if os.path.exists(f):
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Remove old style blocks
        content = re.sub(r'<style>.*?</style>', '', content, flags=re.DOTALL)
        
        # Insert new css block after {% block content %}
        content = content.replace('{% block content %}', '{% block content %}\n' + css_block)
        
        content = content.replace('stats-card', 'stat-card')
        
        # liste-session logic
        content = content.replace('bg-primary-subtle border-0', 'glass-card text-dark')
        content = content.replace('bg-success-subtle border-0', 'glass-card text-dark')
        content = content.replace('bg-warning-subtle border-0', 'glass-card text-dark')
        content = content.replace('bg-info-subtle border-0', 'glass-card text-dark')
        content = content.replace('class="card border-0 shadow-sm rounded-3"', 'class="glass-card"')
        content = content.replace('class="card session-card h-100 border-0 shadow-sm"', 'class="glass-card session-card h-100"')
        content = re.sub(r'bg-gradient-to-r from-primary to-info rounded-3 shadow p-4 text-white', r'glass-card p-4', content)
        content = re.sub(r'bg-white bg-opacity-20 rounded-circle p-3 me-3', r'icon-box bg-primary bg-opacity-10 text-primary me-3', content)
        content = re.sub(r'text-white text-opacity-75', r'text-muted', content)
        content = content.replace('card stats-card', 'stat-card')
        content = content.replace('card stat-card', 'stat-card')

        # Generic bootstrap card to glass-card logic
        # For exams_results and builltins:
        content = content.replace('class="card"', 'class="glass-card"')
        content = content.replace('class="card ', 'class="glass-card ')
        
        # specific to builltins/liste.html:
        content = content.replace('bg-primary rounded fs-3', 'icon-box bg-primary bg-opacity-10 text-primary')
        content = content.replace('btn-soft-primary', 'btn-light btn-rounded text-primary')
        content = content.replace('bg-primary-subtle rounded px-3 py-2', 'filter-bar p-3 border-bottom border-light')

        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Updated {f}")
    else:
        print(f"File not found: {f}")
