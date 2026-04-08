# Structure visuelle du menu SaaS Admin v2.0

## 📐 Layout complet

```
┌─────────────────────────────────────────────────────────────────────┐
│                        APPLICATION SAAS ADMIN                       │
└─────────────────────────────────────────────────────────────────────┘

┌────────────────────────┬────────────────────────────────────────────┐
│   SIDEBAR (280px)      │         MAIN CONTENT AREA                  │
│                        │                                            │
│ ┌────────────────────┐ │  ┌──────────────────────────────────────┐ │
│ │     LOGO BOX       │ │  │        TOP HEADER BAR                │ │
│ │                    │ │  │  [☰] Accueil / SaaS Admin            │ │
│ │  [Image Logo]      │ │  │              [← Retour au portail]   │ │
│ │  SUPER ADMIN       │ │  └──────────────────────────────────────┘ │
│ └────────────────────┘ │                                            │
│ ┌────────────────────┐ │  ┌──────────────────────────────────────┐ │
│ │  QUICK STATS       │ │  │                                      │ │
│ │ 🏢 Tenants: 12     │ │  │        PAGE CONTENT                  │ │
│ │ 👥 Users: 1,245    │ │  │                                      │ │
│ └────────────────────┘ │  │   [Votre contenu ici]                │ │
│ ┌────────────────────┐ │  │                                      │ │
│ │   PRINCIPAL        │ │  │                                      │ │
│ │                    │ │  └──────────────────────────────────────┘ │
│ │ 📊 Tableau de bord │ │                                            │
│ │                    │  ┌──────────────────────────────────────┐ │
│ │ 🏢 Gestion Tenants▼│  │           FOOTER                     │ │
│ │   ├─ Liste         │  │  © 2026 SaaS Admin - SARL Saldae    │ │
│ │   ├─ Créer         │  │  Panel d'Administration Multi-Tenant │ │
│ │   └─ Configs       │  └──────────────────────────────────────┘ │
│ │                    │ │
│ │ 📈 Monitoring ▼    │ │
│ │   ├─ Performance   │ │
│ │   ├─ Stats         │ │
│ │   └─ Alertes [3]   │ │
│ │                    │ │
│ ├──────────────────┤ │
│ │  ADMINISTRATION  │ │
│ │                    │ │
│ │ 🛡️ Licences ▼     │ │
│ │   ├─ Gérer        │ │
│ │   ├─ Plans         │ │
│ │   └─ Facturation   │ │
│ │                    │ │
│ │ 💾 Sauvegardes ▼  │ │
│ │   ├─ Auto          │ │
│ │   ├─ Restaurer     │ │
│ │   └─ Historique    │ │
│ │                    │ │
│ │ ⚙️ Configuration▼  │ │
│ │   ├─ Général       │ │
│ │   ├─ Emails        │ │
│ │   └─ Sécurité      │ │
│ │                    │ │
│ ├──────────────────┤ │
│ │     SYSTÈME      │ │
│ │                    │ │
│ │ 📋 Logs Système    │ │
│ │ 👥 Gestionnaires   │ │
│ │ ❓ Support & Aide  │ │
│ │                    │ │
│ └────────────────────┘ │
│ ┌────────────────────┐ │
│ │   USER PROFILE     │ │
│ │                    │ │
│ │ [AB] John Doe      │ │
│ │      Super Admin   │ │
│ │            [⚙] [⎋] │ │
│ └────────────────────┘ │
│                        │
└────────────────────────┴────────────────────────────────────────────┘
```

---

## 🎨 États visuels des éléments du menu

### État normal
```
┌────────────────────────────┐
│ 📊 Tableau de bord         │  ← Couleur: #475569
└────────────────────────────┘
```

### État survolé
```
┌────────────────────────────┐
│ 📊 Tableau de board    →  │  ← Couleur: #4361ee
└────────────────────────────┘     Background: rgba(67, 97, 238, 0.05)
                                   Transform: translateX(3px)
```

### État actif
```
┌────────────────────────────┐
│ 📊 Tableau de bord         │  ← Couleur: #4361ee
└────────────────────────────┘     Background: rgba(67, 97, 238, 0.1)
                                   Font-weight: 600
                                   Box-shadow: 0 2px 4px rgba(...)
```

### Sous-menu fermé
```
┌────────────────────────────┐
│ 🏢 Gestion des Tenants   ▶│  ← Flèche pointant à droite
└────────────────────────────┘
```

### Sous-menu ouvert
```
┌────────────────────────────┐
│ 🏢 Gestion des Tenants   ▼│  ← Flèche tournée vers le bas
│ ┌──────────────────────┐  │
│ │   ∘ Liste des tenants│  │  ← Background: #f8fafc
│ │   ∘ Créer un tenant  │  │     Padding réduit
│ │   ∘ Configurations   │  │     Point indicateurs
│ └──────────────────────┘  │
└────────────────────────────┘
```

---

## 📱 Responsive : Mobile (<768px)

### Menu fermé (par défaut)
```
┌─────────────────────────────────────────┐
│ [☰] Accueil / SaaS Admin          [←]   │
└─────────────────────────────────────────┘
     ↑
     Menu caché (translateX(-100%))
```

### Menu ouvert (après clic sur ☰)
```
┌──────────────┬──────────────────────────┐
│  MENU (280px)│   OVERLAY (sombre)       │
│              │                          │
│ [×] Fermer   │   Le contenu principal   │
│              │   est grisé et           │
│ STATISTIQUES │   inaccessible           │
│              │                          │
│ PRINCIPAL    │                          │
│ ├─ Dashboard │                          │
│ └─ Tenants   │                          │
│              │                          │
│ [Profile]    │                          │
└──────────────┴──────────────────────────┘
```

---

## 🎯 Composants détaillés

### 1. Badge SUPER ADMIN
```
┌────────────────────┐
│   [LOGO IMAGE]     │
│                    │
│ ┌──────────────┐  │
│ │ SUPER ADMIN  │  │  ← Gradient: #4361ee → #4895ef
│ └──────────────┘  │     Font-size: 0.65rem
└────────────────────┘
```

### 2. Statistiques rapides
```
┌────────────────────────────┐
│ 🏢 Tenants Actifs    12    │  ← Background: dégradé subtil
│ 👥 Utilisateurs     1 245  │     Icônes à gauche
└────────────────────────────┘     Valeurs en gras
```

### 3. Élément avec badge
```
┌────────────────────────────┐
│ 📈 Monitoring        [3] ▶│  ← Badge rouge/rosé
└────────────────────────────┘     Couleur: #f72585
                                   Arrondi: 10px
```

### 4. Profil utilisateur
```
┌────────────────────────────┐
│                            │
│  [AB] John Doe        ⚙ ⎋ │  ← Avatar circulaire
│       Super Admin          │     Initiales en gras
└────────────────────────────┘     Boutons d'action
```

---

## 🔄 Animations

### Ouverture/fermeture sous-menu
```
État initial:                    État final:
┌──────────────┐                ┌──────────────┐
│ Menu Item  ▶ │      →         │ Menu Item  ▼ │
└──────────────┘                └──────────────┘
                                   [Sous-élément]
                                   [Sous-élément]
Durée: 0.3s ease                 Hauteur: auto
Transform: rotate(0)             Transform: rotate(90deg)
```

### Survol d'un élément
```
État normal:                     État survolé:
┌──────────────┐                ┌──────────────┐
│ → Menu Item  │      →         │  → Menu Item │
└──────────────┘                └──────────────┘
X: 0                             X: +3px
Couleur: #475569                 Couleur: #4361ee
Background: transparent           Background: rgba(...)
```

---

## 🎨 Palette de couleurs

### Couleurs principales
```
Primaire:      #4361ee  ████████
Primaire hover: #3a56d4 ████████
Secondaire:    #3f37c9  ████████
Accent:        #4895ef  ████████
Succès:        #4cc9f0  ████████
Avertissement: #f72585  ████████
Info:          #480ca8  ████████
Danger:        #ef233c  ████████
```

### Couleurs du menu
```
Background:    #ffffff  ████████
Item:          #475569  ████████
Hover:         #4361ee  ████████
Actif bg:      rgba(67,97,238,0.1) ░░░░░░░░░░
Bordure:       #e2e8f0  ████████
Sous-menu bg:  #f8fafc  ████████
```

---

## 📊 Hiérarchie des sections

```
Niveau 1: PRINCIPAL (toujours visible)
  ├─ Tableau de bord (accès direct)
  ├─ Gestion des Tenants (sous-menu)
  └─ Monitoring (sous-menu avec badge)

Niveau 2: ADMINISTRATION (séparé par divider)
  ├─ Licences & Abonnements
  ├─ Sauvegardes
  └─ Configuration

Niveau 3: SYSTÈME (séparé par divider)
  ├─ Logs Système
  ├─ Gestionnaires
  └─ Support & Aide
```

---

## 🔗 Flux de navigation

### Exemple: Accéder à la liste des tenants
```
1. Utilisateur clique sur "Gestion des Tenants ▼"
   ↓
2. Le sous-menu se déploie (animation 0.3s)
   ↓
3. Utilisateur clique sur "Liste des tenants"
   ↓
4. Navigation vers: /saas-admin/tenants/
   ↓
5. La page se charge
   ↓
6. Le menu marque automatiquement l'élément comme actif
```

---

## 📐 Dimensions

### Desktop
```
Largeur menu:        280px (configurable)
Hauteur logo:        ~80px
Hauteur stats:       ~70px
Hauteur profil:      ~70px
Padding éléments:    0.75rem 1rem
Espacement éléments: 0.125rem
Icônes:              1.2rem (min-width: 2rem)
```

### Mobile
```
Menu:                Caché par défaut
Overlay:             100% width/height
Bouton toggle:       Visible dans le header
```

---

**Version**: 2.0  
**Dernière mise à jour**: Avril 2026  
**Auteur**: SARL Saldae Systems
