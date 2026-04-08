# Guide d'intégration du menu SaaS Admin

## 🎯 Objectif

Ce guide explique comment intégrer et utiliser la nouvelle structure de menu améliorée dans l'application SaaS Admin.

---

## 📦 Prérequis

1. **Bootstrap 5.3.2** doit être chargé dans le template de base
2. **jQuery** doit être disponible
3. **Remix Icons** doit être chargé pour les icônes

---

## 🚀 Intégration dans une vue

### Étape 1: Passer les statistiques au menu

Dans votre vue Django (ex: `views.py`):

```python
@user_passes_test(superadmin_only, login_url='/saas-admin/login/')
def saas_dashboard_view(request):
    # ... votre logique existante ...
    
    context = {
        'metrics_list': metrics_list,
        'total_db_size': format_size(total_db_bytes),
        'total_media_size': format_size(total_media_bytes),
        'total_users': total_users,
        'nombre_instances': len(instituts),
    }
    
    return render(request, 'saas_admin_app/saas_dashboard.html', context)
```

### Étape 2: Afficher les statistiques dans le template

Dans `saas_dashboard.html`, ajoutez ce script au début du block content:

```html
{% block content %}
<script>
    // Pass dashboard stats to menu
    window.saasStats = {
        tenants: {{ nombre_instances }},
        users: {{ total_users }}
    };
</script>

<!-- Le reste de votre contenu -->
{% endblock %}
```

---

## 🔗 Ajouter de nouvelles URLs au menu

### Étape 1: Créer les vues dans `views.py`

```python
@user_passes_test(superadmin_only, login_url='/saas-admin/login/')
def tenant_list_view(request):
    """Vue pour la liste des tenants."""
    # Logique ici
    return render(request, 'saas_admin_app/tenant_list.html')
```

### Étape 2: Ajouter les URLs dans `urls.py`

```python
from django.urls import path
from .views import saas_dashboard_view, saas_login_view, tenant_list_view

app_name = 'saas_admin_app'

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='saas_admin_app:saas_login', permanent=False)),
    path('login/', saas_login_view, name='saas_login'),
    path('dashboard/', saas_dashboard_view, name='saas_dashboard'),
    path('tenants/', tenant_list_view, name='tenant_list'),  # Nouvelle URL
]
```

### Étape 3: Mettre à jour le menu

Dans `saas_menu.html`, remplacez les `#` par les vraies URLs:

```html
<li class="nav-item">
    <a href="{% url 'saas_admin_app:tenant_list' %}" class="nav-link">
        <span>Liste des tenants</span>
    </a>
</li>
```

---

## 🎨 Personnalisation avancée

### Changer les couleurs du thème

Modifiez les variables CSS dans `saas_menu.html`:

```css
:root {
    --saas-menu-width: 280px;
    --saas-menu-bg: #ffffff;
    --saas-menu-item-color: #475569;
    --saas-menu-item-hover-color: #4361ee;
    --saas-menu-item-active-bg: rgba(67, 97, 238, 0.1);
    --saas-menu-item-active-color: #4361ee;
}
```

### Ajouter une section au menu

Ajoutez une nouvelle section dans `saas_menu.html`:

```html
<div class="saas-menu-divider"></div>

<div class="saas-menu-title">
    <span>Nouvelle Section</span>
</div>

<li class="nav-item">
    <a href="#" class="nav-link">
        <i class="ri-new-icon"></i>
        <span>Nouvel élément</span>
    </a>
</li>
```

### Ajouter un badge de notification

```html
<li class="nav-item">
    <a class="nav-link" data-bs-toggle="collapse" href="#submenu">
        <i class="ri-icon"></i>
        <span>Menu avec notifications</span>
        <span class="menu-badge">5</span>  <!-- Badge -->
        <i class="ri-arrow-right-s-line arrow"></i>
    </a>
</li>
```

---

## 📱 Gestion du responsive

Le menu est automatiquement responsive:

- **Desktop** : Menu visible de 280px
- **Mobile** : Menu caché, accessible via le bouton hamburger

Pour personnaliser le comportement mobile, modifiez les media queries dans `saas_menu.html`.

---

## 🐛 Dépannage

### Problème: Les sous-menus ne s'ouvrent pas

**Solution**: Vérifiez que Bootstrap JS est chargé dans `saas_base.html`:

```html
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
```

### Problème: Les statistiques ne s'affichent pas dans le menu

**Solution**: 
1. Vérifiez que `window.saasStats` est défini dans le template enfant
2. Ouvrez la console du navigateur pour déboguer
3. Assurez-vous que le script est exécuté après le chargement du DOM

### Problème: Les icônes ne s'affichent pas

**Solution**: Vérifiez que Remix Icons est chargé dans `saas_base.html`:

```html
<link href="{% static 'design/assets/css/icons.min.css' %}" rel="stylesheet" type="text/css" />
```

---

## 📊 Exemple complet d'intégration

### Vue (`views.py`):

```python
@user_passes_test(superadmin_only)
def dashboard(request):
    instituts = Institut.objects.all()
    total_users = User.objects.count()
    
    context = {
        'nombre_instances': instituts.count(),
        'total_users': total_users,
    }
    return render(request, 'saas_admin_app/saas_dashboard.html', context)
```

### Template (`saas_dashboard.html`):

```html
{% extends 'saas_admin_app/saas_base.html' %}
{% load static %}

{% block title %}Tableau de bord{% endblock %}

{% block content %}
<script>
    window.saasStats = {
        tenants: {{ nombre_instances }},
        users: {{ total_users }}
    };
</script>

<div class="container-fluid">
    <h1>Tableau de bord SaaS</h1>
    <!-- Votre contenu ici -->
</div>
{% endblock %}
```

---

## 🎓 Bonnes pratiques

1. **Toujours définir `window.saasStats`** dans les vues qui étendent `saas_base.html`
2. **Utiliser les URLs nommées** avec `{% url 'app:name' %}` pour éviter les erreurs
3. **Garder le menu à jour** quand de nouvelles fonctionnalités sont ajoutées
4. **Tester sur mobile** pour vérifier le responsive
5. **Utiliser les icônes Remix** pour la cohérence visuelle

---

## 📞 Support

Pour toute question ou problème:
- Vérifiez la documentation dans `MENU_IMPROVEMENTS.md`
- Consultez les commentaires dans le code de `saas_menu.html`
- Contactez l'équipe de développement SARL Saldae Systems

---

**Version**: 1.0  
**Dernière mise à jour**: Avril 2026
