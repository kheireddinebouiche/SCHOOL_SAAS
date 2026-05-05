# Implementation Plan: LMD (University) Compatibility Framework

This plan outlines the steps to adapt the current SCHOOL_SAAS architecture for University systems (LMD standard), while maintaining backward compatibility for existing "School" clients.

## User Decisions & Constraints

> [!IMPORTANT]
> **Type d'Établissement :** Le choix entre "École / Institut" et "Université (LMD)" sera fixé **une seule fois lors de la création du tenant** dans l'interface SaaS Admin. Cela garantit la cohérence des données pédagogiques et financières sur tout le cycle de vie du tenant.

## User Review Required

> [!WARNING]
> **Règles de Compensation :** Les règles de compensation (passage avec dettes, compensation entre UE) varient parfois selon les universités. Mon moteur de délibération suivra le standard LMD standard (Algérie/France), mais des ajustements pourraient être nécessaires.

## Proposed Changes

### 1. Global Configuration & Architecture

#### [MODIFY] [institut_app/models.py](file:///c:/Users/kheir/Documents/saldae/SCHOOL_SAAS/institut_app/models.py)
- Add `SCHOOL_TYPE_CHOICES = [('school', 'École / Institut'), ('university', 'Université (LMD)')]` to `GlobalConfiguration`.
- Add `school_type` field to `GlobalConfiguration` (default: `'school'`).
- This field will conditionally show/hide menus and change logic across the apps.

---

### 2. Pedagogical Structure (LMD Hierarchy)

#### [NEW] [t_formations/models_lmd.py] (or integrate into models.py)
- **Model `Faculte`**: (Label, Code, Responsable).
- **Model `Departement`**: (Label, Code, Faculte, Responsable).
- **Model `UniteEnseignement (UE)`**:
    - Fields: Label, Code, Type (Fondamentale, Méthodologique, Découverte, Transversale), Credits ECTS, Coefficient, Specialite, Semestre.

#### [MODIFY] [t_formations/models.py](file:///c:/Users/kheir/Documents/saldae/SCHOOL_SAAS/t_formations/models.py)
- Update `Specialites`: Add optional FK to `Departement`.
- Update `Modules`:
    - Add FK to `UniteEnseignement` (UE).
    - Add fields: `credits_ects` (Decimal), `volume_cm` (Hours), `volume_td` (Hours), `volume_tp` (Hours).
    - Update `generate_code` to support University prefixes if `school_type == 'university'`.

---

### 3. Student & Registration Enhancements

#### [MODIFY] [t_etudiants/models.py](file:///c:/Users/kheir/Documents/saldae/SCHOOL_SAAS/t_etudiants/models.py)
- Add `matricule_universitaire` (Unique identifier).
- Add `statut_lmd` (Initial, Redoublant, En Dette).
- Integrate "Dette" tracking: Link students to modules they failed in previous years.

---

### 4. Deliberation Engine & Grade Calculation

#### [NEW] [t_exam/logic_lmd.py]
- Implement `calculer_moyenne_ue(student, ue, session)`: Weighted average of modules within UE.
- Implement `calculer_moyenne_semestre(student, semestre, session)`: Weighted average of UEs.
- Implement `appliquer_compensation(student, semestre)`: Logic to validate a semester if average >= 10, granting all credits.

#### [MODIFY] [t_exam/models.py](file:///c:/Users/kheir/Documents/saldae/SCHOOL_SAAS/t_exam/models.py)
- **Model `Deliberation`**: To store the official "PV de Délibération" per group/semester.
- **Model `CreditAcquis`**: To track ECTS accumulated by each student.

---

### 5. UI/UX Modernization

#### [MODIFY] [Templates & Views]
- Inject `school_type` in context processors to adapt sidebars.
- Create new LMD-specific views for:
    - Curriculum management (UE/Module grid).
    - Deliberation interface (Matrix of grades with compensation highlights).
    - University Transcript (Official PDF export).

## Verification Plan

### Automated Tests
- `python manage.py test t_exam.tests_lmd`: Test compensation logic with various grade scenarios.
- `python manage.py test t_formations.tests_hierarchy`: Verify Faculty -> Dept -> Speciality link.

### Manual Verification
1. Create a "University" tenant.
2. Define a pedagogical structure (Faculté des Sciences -> Département Informatique -> Licence ISIL).
3. Create UEs and Modules with ECTS.
4. Input sample grades for a student.
5. Trigger deliberation and verify that compensation is applied (e.g., student has 9.5 in UE1 and 10.5 in UE2 -> Semester average 10 -> Semester validated).
6. Generate University Transcript and verify ECTS display.
