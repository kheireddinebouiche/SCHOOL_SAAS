import os
import math
import psutil
import platform
import time
import glob
from datetime import datetime
from django.shortcuts import render
from django.db import connection
from django.conf import settings
from django.http import JsonResponse
from django.core.mail import send_mail, EmailMessage
from app.models import Institut
from django_tenants.utils import tenant_context
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from .models import DatabaseBackup, SaaSEmailConfiguration, SaaSMaintenanceConfiguration
from .utils_backup import perform_backup, perform_restore



def superadmin_only(user):
    return user.is_authenticated and user.is_superuser

def get_schema_size_bytes(schema_name):
    """Calcule la taille du schéma en bytes (bases de données PostgreSQL)."""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT SUM(pg_total_relation_size(quote_ident(schemaname) || '.' || quote_ident(tablename)))
            FROM pg_tables
            WHERE schemaname = %s;
        """, [schema_name])
        row = cursor.fetchone()
        return row[0] if (row and row[0]) else 0

def format_size(size_bytes):
    """Formate une taille de fichier en format lisible par l'homme."""
    if not size_bytes or size_bytes == 0:
        return "0 MB"
    
    # Convertir en float pour éviter les erreurs avec les types Decimal
    size_bytes = float(size_bytes)
    
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

def get_directory_size(directory):
    """Calcule la taille totale d'un dossier en bytes."""
    total_size = 0
    if not os.path.exists(directory):
        return total_size
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                try:
                    total_size += os.path.getsize(fp)
                except Exception:
                    pass
    return total_size

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages


def saas_login_view(request):
    """Vue dédiée à la connexion au SaaS Admin Dashboard."""
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('saas_admin_app:saas_dashboard')
        
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('saas_admin_app:saas_dashboard')
            else:
                messages.error(request, 'Accès refusé. Vous devez être un Super Administrateur.')
        else:
            messages.error(request, 'Identifiants invalides.')
            
    return render(request, 'saas_admin_app/login.html')

def saas_logout_view(request):
    """Déconnexion de l'utilisateur superadmin."""
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès.')
    return redirect('saas_admin_app:saas_login')

@user_passes_test(superadmin_only, login_url='/saas-admin/login/')
def saas_dashboard_view(request):
    """Affiche le tableau de bord avec les statistiques de chaque schéma/tenant."""
    instituts = Institut.objects.all().order_by('nom')
    metrics_list = []
    
    total_db_bytes = 0
    total_media_bytes = 0
    total_users = 0

    User = get_user_model()
    
    for institut in instituts:
        schema_name = institut.schema_name
        
        # 1. Taille de la Base de Données
        db_bytes = get_schema_size_bytes(schema_name)
        total_db_bytes += db_bytes
        db_size_formatted = format_size(db_bytes)
        
        # 2. Nombre d'Utilisateurs
        try:
            with tenant_context(institut):
                user_count = User.objects.count()
                total_users += user_count
        except Exception:
            user_count = 0
            
        # 3. Taille des Fichiers Média (fichiers statiques uploader)
        # Assuming the standard django-tenants structure: MEDIA_ROOT / tenant_schema directories
        tenant_media_dir = os.path.join(settings.MEDIA_ROOT, schema_name)
        media_bytes = get_directory_size(tenant_media_dir)
        total_media_bytes += media_bytes
        media_size_formatted = format_size(media_bytes)
        
        # Extraire d'autres détails utiles
        date_creation = institut.date_creation if hasattr(institut, 'date_creation') else None
        
        metrics_list.append({
            'institut': institut,
            'db_size': db_size_formatted,
            'db_bytes': db_bytes,  # Garder la valeur brute pour tri/jauges
            'user_count': user_count,
            'media_size': media_size_formatted,
            'media_bytes': media_bytes,
            'date_creation': date_creation,
        })
        
    context = {
        'metrics_list': metrics_list,
        'total_db_size': format_size(total_db_bytes),
        'total_media_size': format_size(total_media_bytes),
        'total_users': total_users,
        'nombre_instances': len(instituts),
    }
    
    from .models import SaaSMaintenanceConfiguration
    context['maintenance_config'] = SaaSMaintenanceConfiguration.get_solo()

    return render(request, 'saas_admin_app/saas_dashboard.html', context)

@user_passes_test(superadmin_only, login_url='/saas-admin/login/')
def saas_performance_view(request):
    """Affiche les performances système du serveur."""
    
    # CPU Metrics
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count()
    cpu_freq = psutil.cpu_freq()
    cpu_freq_current = cpu_freq.current if cpu_freq else 0
    cpu_freq_max = cpu_freq.max if cpu_freq else 0
    
    # Memory Metrics
    memory = psutil.virtual_memory()
    memory_total = format_size(memory.total)
    memory_used = format_size(memory.used)
    memory_available = format_size(memory.available)
    memory_percent = memory.percent
    
    # Disk Metrics
    disk = psutil.disk_usage('/')
    disk_total = format_size(disk.total)
    disk_used = format_size(disk.used)
    disk_free = format_size(disk.free)
    disk_percent = disk.percent
    
    # Network Metrics
    net_io = psutil.net_io_counters()
    net_bytes_sent = format_size(net_io.bytes_sent)
    net_bytes_recv = format_size(net_io.bytes_recv)
    net_packets_sent = net_io.packets_sent
    net_packets_recv = net_io.packets_recv
    
    # System Info
    system_info = {
        'os': f"{platform.system()} {platform.release()}",
        'architecture': platform.architecture()[0],
        'processor': platform.processor() or 'N/A',
        'hostname': platform.node(),
        'python_version': platform.python_version(),
        'uptime_seconds': int(time.time() - psutil.boot_time()),
    }
    
    # Process Metrics (Django)
    current_process = psutil.Process()
    process_memory = format_size(current_process.memory_info().rss)
    process_cpu = current_process.cpu_percent(interval=0.1)
    process_threads = current_process.num_threads()
    
    # Database Connections
    db_connections = 0
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT count(*) 
                FROM pg_stat_activity 
                WHERE datname = current_database();
            """)
            row = cursor.fetchone()
            db_connections = row[0] if row else 0
    except Exception:
        db_connections = 0
    
    # Tenant Performance Data
    instituts = Institut.objects.all().order_by('nom')
    tenant_metrics = []
    
    for institut in instituts:
        schema_name = institut.schema_name
        
        # Database size
        db_bytes = get_schema_size_bytes(schema_name)
        db_size_formatted = format_size(db_bytes)
        
        # User count
        try:
            with tenant_context(institut):
                User = get_user_model()
                user_count = User.objects.count()
        except Exception:
            user_count = 0
        
        # Active sessions (approximation)
        active_sessions = 0
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT count(*) 
                    FROM pg_stat_activity 
                    WHERE datname = current_database() 
                    AND state = 'active';
                """)
                row = cursor.fetchone()
                active_sessions = row[0] if row else 0
        except Exception:
            active_sessions = 0
        
        tenant_metrics.append({
            'institut': institut,
            'db_size': db_size_formatted,
            'db_bytes': db_bytes,
            'user_count': user_count,
            'active_sessions': active_sessions,
        })
    
    # Sort tenants by DB size (descending)
    tenant_metrics.sort(key=lambda x: x['db_bytes'], reverse=True)
    
    # Calculate uptime
    uptime = system_info['uptime_seconds']
    uptime_days = uptime // 86400
    uptime_hours = (uptime % 86400) // 3600
    uptime_minutes = (uptime % 3600) // 60
    uptime_str = f"{uptime_days}j {uptime_hours}h {uptime_minutes}m"
    
    context = {
        'cpu_percent': cpu_percent,
        'cpu_count': cpu_count,
        'cpu_freq_current': cpu_freq_current,
        'cpu_freq_max': cpu_freq_max,
        'memory_total': memory_total,
        'memory_used': memory_used,
        'memory_available': memory_available,
        'memory_percent': memory_percent,
        'disk_total': disk_total,
        'disk_used': disk_used,
        'disk_free': disk_free,
        'disk_percent': disk_percent,
        'net_bytes_sent': net_bytes_sent,
        'net_bytes_recv': net_bytes_recv,
        'net_packets_sent': net_packets_sent,
        'net_packets_recv': net_packets_recv,
        'system_info': system_info,
        'uptime_str': uptime_str,
        'process_memory': process_memory,
        'process_cpu': process_cpu,
        'process_threads': process_threads,
        'db_connections': db_connections,
        'tenant_metrics': tenant_metrics,
        'timestamp': datetime.now().isoformat(),
    }
    
    return render(request, 'saas_admin_app/saas_performance.html', context)

@user_passes_test(superadmin_only, login_url='/saas-admin/login/')
def saas_logs_view(request):
    """Affiche les logs système de l'application."""
    
    # Get log file paths
    log_files = []
    log_entries = []
    
    # Common log file locations
    possible_log_paths = [
        os.path.join(settings.BASE_DIR, '*.log'),
        os.path.join(settings.BASE_DIR, 'logs', '*.log'),
        os.path.join(settings.BASE_DIR, 'logs', '**', '*.log'),
    ]
    
    # Find all log files
    for pattern in possible_log_paths:
        log_files.extend(glob.glob(pattern, recursive=True))
    
    # Also check for Django log files
    if hasattr(settings, 'LOGGING'):
        log_config = settings.LOGGING
        if 'handlers' in log_config:
            for handler_name, handler_config in log_config['handlers'].items():
                if 'filename' in handler_config:
                    log_file = handler_config['filename']
                    if os.path.exists(log_file) and log_file not in log_files:
                        log_files.append(log_file)
    
    # Get the selected log file (default to first one)
    selected_log_file = request.GET.get('file', log_files[0] if log_files else None)
    log_level_filter = request.GET.get('level', 'ALL')
    search_query = request.GET.get('search', '')
    
    # Read log entries from selected file
    if selected_log_file and os.path.exists(selected_log_file):
        try:
            with open(selected_log_file, 'r', encoding='utf-8', errors='ignore') as f:
                raw_lines = f.readlines()
            
            # Parse log lines (typical Django log format)
            for line in raw_lines:
                line = line.strip()
                if not line:
                    continue
                
                # Determine log level
                level = 'INFO'
                if 'ERROR' in line.upper():
                    level = 'ERROR'
                elif 'WARNING' in line.upper() or 'WARN' in line.upper():
                    level = 'WARNING'
                elif 'DEBUG' in line.upper():
                    level = 'DEBUG'
                elif 'CRITICAL' in line.upper() or 'FATAL' in line.upper():
                    level = 'CRITICAL'
                
                # Apply level filter
                if log_level_filter != 'ALL' and level != log_level_filter:
                    continue
                
                # Apply search filter
                if search_query and search_query.lower() not in line.lower():
                    continue
                
                log_entries.append({
                    'line': line,
                    'level': level,
                    'timestamp': extract_timestamp(line),
                })
        except Exception as e:
            log_entries.append({
                'line': f"Error reading log file: {str(e)}",
                'level': 'ERROR',
                'timestamp': None,
            })
    
    # Get log file statistics
    log_file_stats = []
    for log_file in log_files:
        try:
            file_size = os.path.getsize(log_file)
            file_mod_time = datetime.fromtimestamp(os.path.getmtime(log_file))
            log_file_stats.append({
                'path': log_file,
                'name': os.path.basename(log_file),
                'size': format_size(file_size),
                'modified': file_mod_time,
                'is_selected': log_file == selected_log_file,
            })
        except Exception:
            pass
    
    # Sort log files by modification time (most recent first)
    log_file_stats.sort(key=lambda x: x['modified'], reverse=True)
    
    # Count log levels
    level_counts = {'ERROR': 0, 'WARNING': 0, 'INFO': 0, 'DEBUG': 0, 'CRITICAL': 0}
    for entry in log_entries:
        if entry['level'] in level_counts:
            level_counts[entry['level']] += 1
    
    context = {
        'log_files': log_file_stats,
        'selected_file': selected_log_file,
        'log_entries': log_entries[-500:],  # Limit to last 500 entries for performance
        'level_counts': level_counts,
        'total_entries': len(log_entries),
        'current_level_filter': log_level_filter,
        'search_query': search_query,
    }
    
    return render(request, 'saas_admin_app/saas_logs.html', context)

@user_passes_test(superadmin_only, login_url='/saas-admin/login/')
def saas_processes_view(request):
    """Vue pour afficher les processus système et les services."""
    import subprocess
    import json
    
    # 1. Processus
    processes = []
    # On limite pour éviter de surcharger la page (top CPU/Memory)
    for proc in psutil.process_iter(['pid', 'name', 'username', 'status', 'cpu_percent', 'memory_percent', 'create_time']):
        try:
            pinfo = proc.info
            # Convert timestamp to datetime
            pinfo['uptime'] = datetime.fromtimestamp(pinfo['create_time']).strftime("%Y-%m-%d %H:%M:%S")
            processes.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
            
    # Tri par CPU ou Mémoire (ici par CPU descendant)
    processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
    
    # 2. Services
    services = []
    system_os = platform.system()
    
    if system_os == 'Windows':
        # Utilisation de PowerShell pour obtenir les services
        try:
            cmd = 'powershell -Command "Get-Service | Select-Object Name, DisplayName, Status | ConvertTo-Json"'
            result = subprocess.run(cmd, capture_output=True, shell=True)
            if result.returncode == 0:
                # On décode avec errors='ignore' pour éviter les plantages sur Windows (encoding cp1252 vs powershell output)
                stdout_str = result.stdout.decode('utf-8', errors='ignore')
                raw_services = json.loads(stdout_str)
                # S'il n'y a qu'un service, JSON.loads retourne un dict au lieu d'une liste
                if isinstance(raw_services, dict):
                    raw_services = [raw_services]
                
                for s in raw_services:
                    status_map = {0: 'Stopped', 1: 'StartPending', 2: 'StopPending', 3: 'Running', 4: 'ContinuePending', 5: 'PausePending', 6: 'Paused'}
                    # PowerShell retourne parfois des codes au lieu de strings selon la version
                    status = s.get('Status')
                    if isinstance(status, int):
                        status = status_map.get(status, f"Unknown ({status})")
                    
                    services.append({
                        'name': s.get('Name'),
                        'display_name': s.get('DisplayName'),
                        'status': status,
                        'type': 'Windows Service'
                    })
        except Exception as e:
            services.append({'name': 'Error', 'display_name': f"Could not fetch Windows services: {str(e)}", 'status': 'Error', 'type': 'System'})

    elif system_os == 'Linux':
        # Utilisation de systemctl
        try:
            # On tente de lister les services
            cmd = ['systemctl', 'list-units', '--type=service', '--all', '--no-legend', '--no-pager']
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    parts = line.split(None, 4)
                    if len(parts) >= 4:
                        services.append({
                            'name': parts[0],
                            'display_name': parts[4] if len(parts) > 4 else parts[0],
                            'status': parts[3], # active/inactive/failed
                            'sub_status': parts[2], # running/exited/dead
                            'type': 'Systemd Service'
                        })
        except Exception as e:
            services.append({'name': 'Error', 'display_name': f"Could not fetch Linux services: {str(e)}", 'status': 'Error', 'type': 'System'})

    context = {
        'processes': processes[:100],  # Top 100 processus
        'services': services,
        'system_os': system_os,
        'timestamp': datetime.now().strftime("%H:%M:%S")
    }
    
    return render(request, 'saas_admin_app/saas_processes.html', context)

@user_passes_test(superadmin_only, login_url='/saas-admin/login/')
def saas_terminal_view(request):
    """Affiche la page du terminal système."""
    # Initialiser le répertoire de travail dans la session s'il n'existe pas ou sur demande
    if 'terminal_cwd' not in request.session or request.GET.get('reset') == '1':
        request.session['terminal_cwd'] = str(settings.BASE_DIR)
        
    context = {
        'current_dir': request.session['terminal_cwd'],
        'system_os': platform.system(),
    }
    return render(request, 'saas_admin_app/saas_terminal.html', context)

@user_passes_test(superadmin_only, login_url='/saas-admin/login/')
def saas_terminal_exec_view(request):
    """API endpoint pour exécuter des commandes système avec suivi du répertoire."""
    import subprocess
    import os
    from django.http import JsonResponse
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
    
    command = request.POST.get('command')
    if not command:
        return JsonResponse({'success': False, 'error': 'Commande vide'})
    
    # Récupérer le répertoire actuel depuis la session
    cwd = request.session.get('terminal_cwd', str(settings.BASE_DIR))
    if not os.path.exists(cwd):
        cwd = str(settings.BASE_DIR)
        request.session['terminal_cwd'] = cwd

    system_os = platform.system()
    
    try:
        # Pour supporter le changement de répertoire (cd), on exécute la commande 
        # puis on demande le nouveau chemin (pwd).
        # On utilise un marqueur spécial pour isoler le nouveau CWD.
        cwd_marker = "---SAAS_CWD_MARKER---"
        
        if system_os == 'Windows':
            # Sur Windows (cmd/powershell), cd et pwd fonctionnent différemment
            full_command = f"{command} & echo {cwd_marker} & cd"
        else:
            # Sur Linux (bash/sh), on utilise subshell et pwd
            full_command = f"({command}); echo {cwd_marker}; pwd"
        
        result = subprocess.run(
            full_command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=60,
            encoding='utf-8',
            errors='replace'
        )
        
        stdout = result.stdout
        new_cwd = cwd
        
        # Extraire le nouveau CWD depuis la sortie
        if cwd_marker in stdout:
            parts = stdout.rsplit(cwd_marker, 1)
            stdout = parts[0].strip()
            potential_new_cwd = parts[1].strip()
            if os.path.exists(potential_new_cwd) and os.path.isdir(potential_new_cwd):
                new_cwd = potential_new_cwd
                request.session['terminal_cwd'] = new_cwd
        
        return JsonResponse({
            'success': True,
            'stdout': stdout,
            'stderr': result.stderr,
            'returncode': result.returncode,
            'current_dir': new_cwd
        })
        
    except subprocess.TimeoutExpired:
        return JsonResponse({'success': False, 'error': 'Délai d\'exécution dépassé (60s)'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@user_passes_test(superadmin_only, login_url='/saas-admin/login/')
def saas_explorer_view(request):
    """Affiche la page principale de l'explorateur de fichiers système."""
    initial_path = request.GET.get('path', str(settings.BASE_DIR))
    context = {
        'initial_path': initial_path,
        'system_os': platform.system(),
    }
    return render(request, 'saas_admin_app/saas_explorer.html', context)

@user_passes_test(superadmin_only, login_url='/saas-admin/login/')
def api_explorer_browse(request):
    """API pour lister le contenu d'un répertoire système quelconque."""
    import os
    from django.http import JsonResponse
    
    path = request.GET.get('path', str(settings.BASE_DIR))
    
    # Normalisation pour Windows/Linux
    path = os.path.normpath(path)
    
    if not os.path.exists(path):
        return JsonResponse({'success': False, 'error': 'Chemin inexistant'}, status=404)
    
    if not os.path.isdir(path):
        return JsonResponse({'success': False, 'error': 'N\'est pas un répertoire'}, status=400)
    
    items = []
    try:
        for entry in os.scandir(path):
            try:
                info = entry.stat()
                items.append({
                    'name': entry.name,
                    'is_dir': entry.is_dir(),
                    'size': info.st_size,
                    'size_formatted': format_size(info.st_size) if entry.is_file() else '--',
                    'modified': datetime.fromtimestamp(info.st_mtime).strftime('%d/%m/%Y %H:%M'),
                    'permissions': oct(info.st_mode & 0o777),
                })
            except Exception:
                continue
                
        # Tri : dossiers d'abord, puis fichiers
        items.sort(key=lambda x: (not x['is_dir'], x['name'].lower()))
        
        return JsonResponse({
            'success': True,
            'current_path': path,
            'parent_path': os.path.dirname(path),
            'items': items,
            'sep': os.sep
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@user_passes_test(superadmin_only, login_url='/saas-admin/login/')
def api_explorer_read(request):
    """Lit le contenu d'un fichier texte."""
    import os
    from django.http import JsonResponse
    
    path = request.GET.get('path')
    if not path or not os.path.isfile(path):
        return JsonResponse({'success': False, 'error': 'Fichier invalide'}, status=400)
    
    try:
        # Vérification si binaire (basique)
        with open(path, 'rb') as f:
            chunk = f.read(1024)
            if b'\0' in chunk:
                return JsonResponse({'success': False, 'is_binary': True, 'error': 'Fichier binaire non éditable'})
        
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
            
        return JsonResponse({
            'success': True,
            'content': content,
            'filename': os.path.basename(path),
            'extension': os.path.splitext(path)[1].lower()
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@user_passes_test(superadmin_only, login_url='/saas-admin/login/')
def api_explorer_save(request):
    """Enregistre les modifications d'un fichier."""
    import os
    from django.http import JsonResponse
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
        
    path = request.POST.get('path')
    content = request.POST.get('content', '')
    
    if not path or not os.path.isfile(path):
        return JsonResponse({'success': False, 'error': 'Fichier invalide'}, status=400)
        
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return JsonResponse({'success': True, 'message': 'Fichier enregistré avec succès'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@user_passes_test(superadmin_only, login_url='/saas-admin/login/')
def api_explorer_delete(request):
    """Supprime un fichier ou un répertoire."""
    import os
    import shutil
    from django.http import JsonResponse
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
        
    path = request.POST.get('path')
    if not path or not os.path.exists(path):
        return JsonResponse({'success': False, 'error': 'Chemin invalide'}, status=400)
        
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
        return JsonResponse({'success': True, 'message': 'Suppression effectuée avec succès'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

def extract_timestamp(log_line):
    """Extract timestamp from a log line."""
    try:
        # Try to find common timestamp patterns
        import re
        # Pattern: 2024-01-15 10:30:45 or 2024-01-15T10:30:45
        match = re.search(r'\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}', log_line)
        if match:
            timestamp_str = match.group(0)
            timestamp_str = timestamp_str.replace('T', ' ')
            return datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
    except Exception:
        pass
    return None

@user_passes_test(superadmin_only, login_url='/saas-admin/login/')
def saas_tenant_detail_view(request, tenant_id):
    """Affiche les détails complets d'un tenant/institution."""
    
    # Get the tenant/institut
    try:
        institut = Institut.objects.get(id=tenant_id)
    except Institut.DoesNotExist:
        from django.http import Http404
        raise Http404("Tenant non trouvé")
    
    schema_name = institut.schema_name
    User = get_user_model()
    
    # Basic tenant metrics
    db_bytes = get_schema_size_bytes(schema_name)
    db_size_formatted = format_size(db_bytes)
    
    tenant_media_dir = os.path.join(settings.MEDIA_ROOT, schema_name)
    media_bytes = get_directory_size(tenant_media_dir)
    media_size_formatted = format_size(media_bytes)
    
    # Initialize tenant data
    tenant_data = {
        'institut': institut,
        'db_size': db_size_formatted,
        'db_bytes': db_bytes,
        'media_size': media_size_formatted,
        'media_bytes': media_bytes,
        'users': [],
    }
    
    # Get tenant-specific data using tenant_context
    try:
        with tenant_context(institut):
            # Get all users
            users = User.objects.all().order_by('date_joined')
            for user in users:
                tenant_data['users'].append({
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'is_active': user.is_active,
                    'is_superuser': user.is_superuser,
                    'is_staff': user.is_staff,
                    'date_joined': user.date_joined,
                    'last_login': user.last_login,
                })
            
            tenant_data['user_count'] = users.count()
            
    except Exception as e:
        tenant_data['error'] = str(e)
    
    context = {
        'tenant_data': tenant_data,
    }
    
    return render(request, 'saas_admin_app/saas_tenant_detail.html', context)

@user_passes_test(superadmin_only, login_url='/saas-admin/login/')
def saas_update_user_view(request, tenant_id, user_id):
    """API endpoint pour modifier les informations d'un utilisateur d'un tenant."""
    from django.http import JsonResponse
    from django.views.decorators.http import require_http_methods
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
    
    try:
        institut = Institut.objects.get(id=tenant_id)
    except Institut.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Tenant non trouvé'}, status=404)
    
    try:
        with tenant_context(institut):
            User = get_user_model()
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Utilisateur non trouvé'}, status=404)
            
            # Update user fields
            if 'first_name' in request.POST:
                user.first_name = request.POST['first_name']
            if 'last_name' in request.POST:
                user.last_name = request.POST['last_name']
            if 'email' in request.POST:
                user.email = request.POST['email']
            if 'is_active' in request.POST:
                user.is_active = request.POST['is_active'] == 'true'
            if 'is_superuser' in request.POST:
                user.is_superuser = request.POST['is_superuser'] == 'true'
            if 'is_staff' in request.POST:
                user.is_staff = request.POST['is_staff'] == 'true'
            
            user.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Utilisateur mis à jour avec succès',
                'user': {
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'is_active': user.is_active,
                }
            })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@user_passes_test(superadmin_only, login_url='/saas-admin/login/')
def saas_tenant_files_view(request, tenant_id):
    """Affiche le navigateur de fichiers pour un tenant."""
    try:
        institut = Institut.objects.get(id=tenant_id)
    except Institut.DoesNotExist:
        from django.http import Http404
        raise Http404("Tenant non trouvé")
    
    schema_name = institut.schema_name
    tenant_media_dir = os.path.join(settings.MEDIA_ROOT, schema_name)
    
    context = {
        'institut': institut,
        'tenant_id': tenant_id,
        'schema_name': schema_name,
        'media_root': tenant_media_dir,
        'media_exists': os.path.exists(tenant_media_dir),
    }
    
    return render(request, 'saas_admin_app/saas_tenant_files.html', context)

@user_passes_test(superadmin_only, login_url='/saas-admin/login/')
def saas_file_browser_view(request, tenant_id):
    """API endpoint pour naviguer dans les fichiers d'un tenant."""
    from django.http import JsonResponse
    
    try:
        institut = Institut.objects.get(id=tenant_id)
    except Institut.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Tenant non trouvé'}, status=404)
    
    schema_name = institut.schema_name
    tenant_media_dir = os.path.join(settings.MEDIA_ROOT, schema_name)
    
    # Get the path to browse (relative to tenant media dir)
    rel_path = request.GET.get('path', '')
    
    # Normalize path separators
    rel_path = rel_path.replace('\\', '/')
    
    # Security: prevent path traversal
    abs_path = os.path.normpath(os.path.join(tenant_media_dir, rel_path))
    if not abs_path.startswith(os.path.normpath(tenant_media_dir)):
        return JsonResponse({'success': False, 'error': 'Accès non autorisé'}, status=403)
    
    if not os.path.exists(abs_path):
        return JsonResponse({'success': False, 'error': 'Chemin non trouvé'}, status=404)
    
    files_and_dirs = []
    
    # If it's a file, return file info
    if os.path.isfile(abs_path):
        stat = os.stat(abs_path)
        files_and_dirs.append({
            'name': os.path.basename(abs_path),
            'type': 'file',
            'size': stat.st_size,
            'size_formatted': format_size(stat.st_size),
            'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%d/%m/%Y %H:%M'),
            'path': rel_path,
            'extension': os.path.splitext(abs_path)[1].lower(),
        })
        return JsonResponse({
            'success': True,
            'current_path': rel_path,
            'parent_path': os.path.dirname(rel_path),
            'items': files_and_dirs,
        })
    
    # If it's a directory, list contents
    try:
        for item in sorted(os.listdir(abs_path)):
            item_path = os.path.join(abs_path, item)
            rel_item_path = os.path.relpath(item_path, tenant_media_dir)
            
            # Ensure forward slashes for web URLs (important on Windows)
            rel_item_path = rel_item_path.replace('\\', '/')
            
            stat = os.stat(item_path)
            is_dir = os.path.isdir(item_path)
            
            item_info = {
                'name': item,
                'type': 'directory' if is_dir else 'file',
                'size': stat.st_size if not is_dir else 0,
                'size_formatted': '—' if is_dir else format_size(stat.st_size),
                'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%d/%m/%Y %H:%M'),
                'path': rel_item_path,
            }
            
            if not is_dir:
                item_info['extension'] = os.path.splitext(item)[1].lower()
            
            files_and_dirs.append(item_info)
        
        # Sort: directories first, then files
        files_and_dirs.sort(key=lambda x: (x['type'] != 'directory', x['name'].lower()))
        
        # Calculate parent path
        parent_path = os.path.dirname(rel_path).replace('\\', '/') if rel_path else ''
        
        return JsonResponse({
            'success': True,
            'current_path': rel_path,
            'parent_path': parent_path,
            'items': files_and_dirs,
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@user_passes_test(superadmin_only, login_url='/saas-admin/login/')
def saas_file_serve_view(request, tenant_id, file_path):
    """Sert un fichier spécifique d'un tenant."""
    from django.http import FileResponse, Http404, HttpResponseForbidden
    import mimetypes
    
    try:
        institut = Institut.objects.get(id=tenant_id)
    except Institut.DoesNotExist:
        raise Http404("Tenant non trouvé")
    
    schema_name = institut.schema_name
    tenant_media_dir = os.path.join(settings.MEDIA_ROOT, schema_name)
    
    # Build the absolute file path
    abs_file_path = os.path.normpath(os.path.join(tenant_media_dir, file_path))
    
    # Security check: prevent path traversal
    if not abs_file_path.startswith(os.path.normpath(tenant_media_dir)):
        return HttpResponseForbidden("Accès non autorisé")
    
    if not os.path.exists(abs_file_path):
        raise Http404("Fichier non trouvé")
    
    if not os.path.isfile(abs_file_path):
        raise Http404("Ce n'est pas un fichier")
    
    # Determine content type
    content_type, _ = mimetypes.guess_type(abs_file_path)
    if content_type is None:
        content_type = 'application/octet-stream'
    
    # Serve the file
    response = FileResponse(
        open(abs_file_path, 'rb'),
        content_type=content_type
    )
    response['Content-Disposition'] = f'inline; filename="{os.path.basename(abs_file_path)}"'
    response['Content-Length'] = os.path.getsize(abs_file_path)
    
    # Allow embedding in iframes for preview
    response['X-Frame-Options'] = 'SAMEORIGIN'
    response['Content-Security-Policy'] = "frame-ancestors 'self'"
    
    return response

@user_passes_test(superadmin_only, login_url='/saas-admin/login/')
def saas_reset_user_password_view(request, tenant_id, user_id):
    """API endpoint pour réinitialiser le mot de passe d'un utilisateur."""
    from django.http import JsonResponse
    import secrets
    from .models import SaaSEmailConfiguration
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
    
    # Check if we should send email
    send_email = request.POST.get('send_email', 'false').lower() == 'true'
    
    try:
        institut = Institut.objects.get(id=tenant_id)
    except Institut.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Tenant non trouvé'}, status=404)
    
    try:
        with tenant_context(institut):
            User = get_user_model()
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Utilisateur non trouvé'}, status=404)
            
            # Generate a random password
            new_password = secrets.token_urlsafe(12)
            
            # Set the new password
            user.set_password(new_password)
            user.save()
            
            # Send email if requested and email is enabled
            email_sent = False
            email_error = None
            
            if send_email and user.email:
                try:
                    # Get email configuration from SaaS admin
                    config = SaaSEmailConfiguration.get_solo()
                    
                    if config.email_enabled:
                        # Apply email settings
                        config.apply_email_settings()
                        
                        # Format email content
                        subject = config.email_reset_password_subject
                        message = config.email_reset_password_template.format(
                            user_name=user.get_full_name() or user.username,
                            password=new_password
                        )
                        
                        # Send email
                        send_mail(
                            subject=subject,
                            message=message,
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[user.email],
                            fail_silently=False,
                        )
                        email_sent = True
                    else:
                        email_error = "L'envoi d'emails n'est pas activé dans la configuration"
                except Exception as email_err:
                    email_error = f"Erreur lors de l'envoi: {str(email_err)}"
                    import logging
                    logging.getLogger(__name__).error(f"Email send error: {email_err}")
            
            response_data = {
                'success': True,
                'message': f'Mot de passe réinitialisé pour {user.get_full_name() or user.email}',
                'new_password': new_password,
                'email_sent': email_sent,
                'email_error': email_error,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'full_name': user.get_full_name() or user.username,
                }
            }
            
            return JsonResponse(response_data)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@user_passes_test(superadmin_only, login_url='/saas-admin/login/')
def saas_email_config_view(request):
    """Page de configuration des emails."""
    from .models import SaaSEmailConfiguration
    from django.shortcuts import redirect
    from django.contrib import messages
    
    config = SaaSEmailConfiguration.get_solo()
    
    if request.method == 'POST':
        config.email_enabled = request.POST.get('email_enabled', 'false').lower() == 'true'
        config.email_host = request.POST.get('email_host', 'smtp.gmail.com')
        config.email_port = int(request.POST.get('email_port', 587))
        config.email_use_tls = request.POST.get('email_use_tls', 'true').lower() == 'true'
        config.email_host_user = request.POST.get('email_host_user', '')
        config.email_host_password = request.POST.get('email_host_password', '')
        config.default_from_email = request.POST.get('default_from_email', 'noreply@school-saas.com')
        config.email_reset_password_subject = request.POST.get('email_reset_password_subject', config.email_reset_password_subject)
        config.email_reset_password_template = request.POST.get('email_reset_password_template', config.email_reset_password_template)
        config.save()
        
        messages.success(request, 'Configuration email sauvegardée avec succès')
        return redirect('saas_admin_app:saas_email_config')
    
    context = {
        'config': config,
    }
    
    return render(request, 'saas_admin_app/saas_email_config.html', context)

@user_passes_test(superadmin_only, login_url='/saas-admin/login/')
def saas_test_email_view(request):
    """API pour tester l'envoi d'email."""
    from .models import SaaSEmailConfiguration
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
    
    try:
        config = SaaSEmailConfiguration.get_solo()
        
        if not config.email_enabled:
            return JsonResponse({'success': False, 'error': "L'envoi d'emails n'est pas activé"}, status=400)
        
        # Apply email settings
        config.apply_email_settings()
        
        test_email = request.POST.get('email', config.email_host_user)
        if not test_email:
            return JsonResponse({'success': False, 'error': 'Aucune email de test fournie'}, status=400)
        
        # Send test email
        send_mail(
            subject='Test Email - School SaaS',
            message='Ceci est un email de test pour vérifier la configuration SMTP de School SaaS.\n\nSi vous avez reçu cet email, la configuration fonctionne correctement.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[test_email],
            fail_silently=False,
        )
        
        return JsonResponse({
            'success': True,
            'message': f'Email de test envoyé avec succès à {test_email}'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@user_passes_test(superadmin_only, login_url='/saas-admin/login/')
def saas_toggle_maintenance_view(request):
    """API endpoint pour basculer le mode de développement/maintenance."""
    from .models import SaaSMaintenanceConfiguration
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
    
    try:
        config = SaaSMaintenanceConfiguration.get_solo()
        
        # Le frontend nous envoie 'true' ou 'false' sous forme de chaine
        is_maintenance = request.POST.get('is_maintenance_mode', 'false').lower() == 'true'
        config.is_maintenance_mode = is_maintenance
        
        # Récupération optionnelle du message et de l'heure de fin
        message = request.POST.get('maintenance_message')
        if message:
            config.maintenance_message = message
            
        end_time_raw = request.POST.get('maintenance_end_time')
        if end_time_raw:
            try:
                # Le format envoyé par datetime-local est souvent YYYY-MM-DDTHH:MM
                from django.utils.dateparse import parse_datetime
                config.maintenance_end_time = parse_datetime(end_time_raw)
            except Exception:
                config.maintenance_end_time = None
        else:
            config.maintenance_end_time = None
            
        config.save()
        
        status_text = "activé" if is_maintenance else "désactivé"
        return JsonResponse({
            'success': True,
            'message': f'Mode de développement (maintenance) {status_text} avec succès.',
            'is_maintenance_mode': config.is_maintenance_mode,
            'maintenance_end_time': config.maintenance_end_time.isoformat() if config.maintenance_end_time else None
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@user_passes_test(superadmin_only, login_url='/saas-admin/login/')
def saas_backups_view(request):
    """Affiche la liste des sauvegardes effectuées."""
    backups = DatabaseBackup.objects.all()
    
    # Statistiques simples
    total_backups = backups.count()
    global_backups = backups.filter(backup_type='GLOBAL').count()
    tenant_backups = backups.filter(backup_type='TENANT').count()
    total_size = sum(b.size for b in backups)
    
    context = {
        'backups': backups,
        'instituts': Institut.objects.all().order_by('nom'),
        'total_backups': total_backups,
        'global_backups': global_backups,
        'tenant_backups': tenant_backups,
        'total_size_formatted': format_size(total_size),
    }
    return render(request, 'saas_admin_app/saas_backups.html', context)

@user_passes_test(superadmin_only, login_url='/saas-admin/login/')
def saas_create_backup_view(request):
    """Déclenche une nouvelle sauvegarde."""
    tenant_id = request.GET.get('tenant_id')
    tenant = None
    
    if tenant_id:
        try:
            tenant = Institut.objects.get(id=tenant_id)
        except Institut.DoesNotExist:
            messages.error(request, "Tenant non trouvé.")
            return redirect('saas_admin_app:saas_backups')
    
    success, result = perform_backup(tenant)
    
    if success:
        messages.success(request, f"Sauvegarde {'globale' if not tenant else f'du tenant {tenant.nom}'} réussie.")
    else:
        messages.error(request, f"Échec de la sauvegarde : {result}")
        
    return redirect('saas_admin_app:saas_backups')

@user_passes_test(superadmin_only, login_url='/saas-admin/login/')
def saas_delete_backup_view(request, backup_id):
    """Supprime une sauvegarde spécifique."""
    try:
        backup = DatabaseBackup.objects.get(id=backup_id)
        filename = backup.filename
        backup.delete()  # Ceci supprimera aussi le fichier physique via la méthode delete du modèle
        messages.success(request, f"Sauvegarde {filename} supprimée.")
    except DatabaseBackup.DoesNotExist:
        messages.error(request, "Sauvegarde non trouvée.")
        
    return redirect('saas_admin_app:saas_backups')

@user_passes_test(superadmin_only, login_url='/saas-admin/login/')
def saas_download_backup_view(request, backup_id):
    """Permet de télécharger un fichier de sauvegarde."""
    from django.http import FileResponse, Http404
    try:
        backup = DatabaseBackup.objects.get(id=backup_id)
        if backup.file and os.path.exists(backup.file.path):
            return FileResponse(open(backup.file.path, 'rb'), as_attachment=True, filename=backup.filename)
        else:
            messages.error(request, "Fichier physique introuvable.")
            return redirect('saas_admin_app:saas_backups')
    except DatabaseBackup.DoesNotExist:
        raise Http404("Sauvegarde non trouvée.")


@user_passes_test(superadmin_only, login_url='/saas-admin/login/')
def saas_restore_backup_view(request, backup_id):
    """Effectue la restauration d'une sauvegarde de tenant."""
    from django.shortcuts import get_object_or_404, redirect
    from django.contrib import messages
    
    if request.method != 'POST':
        messages.error(request, "Méthode non autorisée.")
        return redirect('saas_admin_app:saas_backups')
        
    backup_obj = get_object_or_404(DatabaseBackup, id=backup_id)
    
    # Sécurité supplémentaire : vérification du code de confirmation
    confirmation_code = request.POST.get('confirmation_code')
    if confirmation_code != backup_obj.filename:
        messages.error(request, "Le code de confirmation est incorrect. Veuillez saisir le nom complet du fichier.")
        return redirect('saas_admin_app:saas_backups')

    # 1. Activer le mode maintenance
    maintenance_config = SaaSMaintenanceConfiguration.get_solo()
    old_maintenance_state = maintenance_config.is_maintenance_mode
    maintenance_config.is_maintenance_mode = True
    maintenance_config.maintenance_message = f"Restauration en cours pour {backup_obj.tenant.nom if backup_obj.tenant else 'un tenant'}. Veuillez patienter..."
    maintenance_config.save()
    
    try:
        # 2. Effectuer la restauration
        success, message = perform_restore(backup_obj)
        
        if success:
            messages.success(request, f"Succès : {message}")
        else:
            messages.error(request, f"Échec de la restauration : {message}")
            
    finally:
        # 3. Restaurer l'état précédent du mode maintenance
        maintenance_config.is_maintenance_mode = old_maintenance_state
        maintenance_config.save()
        
    return redirect('saas_admin_app:saas_backups')




