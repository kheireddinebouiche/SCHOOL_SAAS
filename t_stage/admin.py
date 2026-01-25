from django.contrib import admin
from .models import Stage, FocusGroup, SeanceFocusGroup, PresentationProgressive, ConseilValidation, DecisionConseil

@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ('get_etudiants', 'groupe', 'encadrant', 'sujet', 'taux_avancement', 'statut')
    list_filter = ('statut', 'encadrant', 'groupe')
    search_fields = ('sujet', 'etudiants__nom')

    def get_etudiants(self, obj):
        return ", ".join([str(e) for e in obj.etudiants.all()])
    get_etudiants.short_description = 'Étudiants'

class SeanceFocusGroupInline(admin.TabularInline):
    model = SeanceFocusGroup
    extra = 1

@admin.register(FocusGroup)
class FocusGroupAdmin(admin.ModelAdmin):
    list_display = ('nom', 'encadrant', 'thematique', 'date_creation')
    list_filter = ('encadrant',)
    inlines = [SeanceFocusGroupInline]

@admin.register(PresentationProgressive)
class PresentationProgressiveAdmin(admin.ModelAdmin):
    list_display = ('stage', 'etape', 'date_presentation', 'taux_avancement_declare', 'validee')
    list_filter = ('etape', 'validee')

class DecisionConseilInline(admin.TabularInline):
    model = DecisionConseil
    extra = 1

@admin.register(ConseilValidation)
class ConseilValidationAdmin(admin.ModelAdmin):
    list_display = ('date_conseil',)
    inlines = [DecisionConseilInline]
