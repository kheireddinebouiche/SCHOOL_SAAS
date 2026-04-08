# 📊 Statistiques dynamiques dans le menu

## Vue d'ensemble

Le menu SaaS Admin affiche maintenant des statistiques en temps réel dans sa section supérieure. Ces statistiques sont passées dynamiquement depuis le tableau de bord.

---

## 🔧 Comment ça fonctionne

### 1. Flux de données

```
┌─────────────────────┐
│   Vue Django        │
│   (views.py)        │
└──────────┬──────────┘
           │
           │ Context:
           │ - nombre_instances
           │ - total_users
           ↓
┌─────────────────────┐
│   Template          │
│   (dashboard.html)  │
└──────────┬──────────┘
           │
           │ Window object:
           │ window.saasStats
           ↓
┌─────────────────────┐
│   Menu Template     │
│   (saas_menu.html)  │
└──────────┬──────────┘
           │
           │ JavaScript:
           │ DOMContentLoaded
           ↓
┌─────────────────────┐
│   Quick Stats       │
│   Section           │
│   • Tenants: XX     │
│   • Users: XXX      │
└─────────────────────┘
```

---

## 📝 Implémentation

### Étape 1: Dans la vue Django

Fichier: `saas_admin_app/views.py`

```python
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
        # ... votre logique existante ...
        total_users += user_count
        # ... suite de votre logique ...
    
    context = {
        'metrics_list': metrics_list,
        'total_db_size': format_size(total_db_bytes),
        'total_media_size': format_size(total_media_bytes),
        'total_users': total_users,              # ← Important
        'nombre_instances': len(instituts),      # ← Important
    }
    
    return render(request, 'saas_admin_app/saas_dashboard.html', context)
```

### Étape 2: Dans le template dashboard

Fichier: `templates/saas_admin_app/saas_dashboard.html`

```html
{% extends 'saas_admin_app/saas_base.html' %}
{% load static %}
{% block title %} SaaS Command Center {% endblock title %}
{% block content %}

<!-- Script pour passer les statistiques au menu -->
<script>
    window.saasStats = {
        tenants: {{ nombre_instances }},
        users: {{ total_users }}
    };
</script>

<!-- Le reste de votre contenu -->
<div class="main-content">
    ...
</div>
{% endblock content %}
```

### Étape 3: Le menu met à jour automatiquement

Fichier: `templates/saas_admin_app/saas_menu.html`

```javascript
document.addEventListener('DOMContentLoaded', function() {
    const statsSection = document.querySelector('.saas-quick-stats');
    
    if (statsSection && typeof window.saasStats !== 'undefined') {
        const tenants = window.saasStats.tenants || 0;
        const users = window.saasStats.users || 0;
        
        statsSection.innerHTML = `
            <div class="stat-item">
                <span class="stat-label">
                    <i class="ri-building-4-line me-1"></i> Tenants
                </span>
                <span class="stat-value">${tenants}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">
                    <i class="ri-group-line me-1"></i> Utilisateurs
                </span>
                <span class="stat-value">${users.toLocaleString('fr-FR')}</span>
            </div>
        `;
    }
});
```

---

## 🎨 Résultat visuel

### Avant (statiques)
```
┌────────────────────────────┐
│ 🏢 Tenants Actifs    --    │
│ 👥 Utilisateurs      --    │
└────────────────────────────┘
```

### Après (dynamiques)
```
┌────────────────────────────┐
│ 🏢 Tenants           12    │
│ 👥 Utilisateurs   1 245    │
└────────────────────────────┘
```

---

## 📊 Formatage des nombres

### Nombre français (fr-FR)
- Séparateur de milliers: espace insécable
- Pas de décimales pour les comptesurs

**Exemples:**
- `1000` → `1 000`
- `1234567` → `1 234 567`
- `42` → `42`

### Personnalisation du format

Pour changer le format de localisation, modifiez:

```javascript
users.toLocaleString('fr-FR')  // Format français
users.toLocaleString('en-US')  // Format américain: 1,234,567
users.toLocaleString('de-DE')  // Format allemand: 1.234.567
```

---

## 🔍 Dépannage

### Problème: Les statistiques affichent 0

**Causes possibles:**
1. La vue ne passe pas `nombre_instances` ou `total_users` dans le context
2. Le script est exécuté avant que `window.saasStats` ne soit défini
3. Il y a une erreur JavaScript dans la console

**Solution:**

```javascript
// Debug: Vérifiez dans la console du navigateur
console.log('saasStats:', window.saasStats);

// Vérifiez que les variables Django sont bien définies
<script>
    console.log('Tenants:', {{ nombre_instances }});
    console.log('Users:', {{ total_users }});
    
    window.saasStats = {
        tenants: {{ nombre_instances }},
        users: {{ total_users }}
    };
</script>
```

### Problème: Erreur JavaScript

Si vous voyez: `Unexpected token ';'`

**Cause:** Les variables Django ne sont pas définies

**Solution:** Assurez-vous que la vue passe bien le context:

```python
def ma_vue(request):
    context = {
        'nombre_instances': 10,  # ← Doit être défini
        'total_users': 500,      # ← Doit être défini
    }
    return render(request, 'mon_template.html', context)
```

### Problème: Le formatage ne fonctionne pas

**Solution:** Utilisez un fallback:

```javascript
const users = window.saasStats.users || 0;
const formattedUsers = users.toLocaleString ? 
    users.toLocaleString('fr-FR') : 
    users.toString();
```

---

## 🚀 Statistiques avancées

### Ajouter plus de statistiques

#### 1. Dans la vue (views.py)

```python
context = {
    'nombre_instances': len(instituts),
    'total_users': total_users,
    'total_db_size': format_size(total_db_bytes),
    'total_media_size': format_size(total_media_bytes),
    'active_tenants': active_tenants.count(),  # Nouveau
    'storage_used': total_storage,              # Nouveau
}
```

#### 2. Dans le template dashboard (dashboard.html)

```html
<script>
    window.saasStats = {
        tenants: {{ nombre_instances }},
        users: {{ total_users }},
        activeTenants: {{ active_tenants }},
        storageUsed: {{ total_db_size|safe }}  // "safe" pour éviter l'échappement
    };
</script>
```

#### 3. Dans le menu (saas_menu.html)

```javascript
statsSection.innerHTML = `
    <div class="stat-item">
        <span class="stat-label">
            <i class="ri-building-4-line me-1"></i> Tenants
        </span>
        <span class="stat-value">${tenants}</span>
    </div>
    <div class="stat-item">
        <span class="stat-label">
            <i class="ri-group-line me-1"></i> Utilisateurs
        </span>
        <span class="stat-value">${users.toLocaleString('fr-FR')}</span>
    </div>
    <div class="stat-item">
        <span class="stat-label">
            <i class="ri-check-line me-1"></i> Actifs
        </span>
        <span class="stat-value">${activeTenants}</span>
    </div>
`;
```

---

## 📈 Statistiques en temps réel (AJAX)

Pour des mises à jour en temps réel sans recharger la page:

### 1. Créer une vue API

```python
from django.http import JsonResponse

def saas_stats_api(request):
    """API retournant les statistiques en temps réel."""
    return JsonResponse({
        'tenants': Institut.objects.count(),
        'users': User.objects.count(),
        'active_tenants': Institut.objects.filter(is_active=True).count(),
    })
```

### 2. Ajouter l'URL

```python
path('api/stats/', saas_stats_api, name='stats_api'),
```

### 3. Mettre à jour le menu avec polling

```javascript
function updateStats() {
    fetch('/saas-admin/api/stats/')
        .then(response => response.json())
        .then(data => {
            const statsSection = document.querySelector('.saas-quick-stats');
            statsSection.innerHTML = `
                <div class="stat-item">
                    <span class="stat-label">
                        <i class="ri-building-4-line me-1"></i> Tenants
                    </span>
                    <span class="stat-value">${data.tenants}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">
                        <i class="ri-group-line me-1"></i> Utilisateurs
                    </span>
                    <span class="stat-value">${data.users.toLocaleString('fr-FR')}</span>
                </div>
            `;
        });
}

// Mettre à jour toutes les 30 secondes
setInterval(updateStats, 30000);

// Première mise à jour immédiate
updateStats();
```

---

## 🎯 Bonnes pratiques

1. ✅ **Toujours définir des valeurs par défaut**
   ```javascript
   const tenants = window.saasStats?.tenants || 0;
   ```

2. ✅ **Utiliser `toLocaleString` pour les grands nombres**
   ```javascript
   users.toLocaleString('fr-FR')  // 1 234 567
   ```

3. ✅ **Vérifier l'existence de l'objet avant d'accéder aux propriétés**
   ```javascript
   if (typeof window.saasStats !== 'undefined') { ... }
   ```

4. ✅ **Utiliser le template literal pour l'HTML dynamique**
   ```javascript
   `Valeur: ${variable}`  // Au lieu de 'Valeur: ' + variable
   ```

5. ✅ **Formater côté serveur pour les chaînes complexes**
   ```python
   'total_db_size': format_size(total_db_bytes)  # "1.5 GB"
   ```

---

## 📚 Ressources

- [Django Templates Documentation](https://docs.djangoproject.com/en/stable/topics/templates/)
- [JavaScript toLocaleString](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/toLocaleString)
- [Bootstrap Collapse](https://getbootstrap.com/docs/5.3/components/collapse/)

---

**Version**: 1.0  
**Dernière mise à jour**: Avril 2026  
**Auteur**: SARL Saldae Systems
