from django.contrib import admin
from .models import *

class LignesDevisInlines(admin.TabularInline):
    model = LignesDevis
    extra = 0

class DevisAdmin(admin.ModelAdmin):
    inlines = [LignesDevisInlines]
    list_display = ('num_devis', 'client', 'montant', 'etat')

class LignesFactureInlines(admin.TabularInline):
    model = LignesFacture
    extra = 0

class FactureAdmin(admin.ModelAdmin):
    inlines = [LignesFactureInlines]
    list_display = ('num_facture', 'client', 'total_ttc', 'etat')

admin.site.register(Thematiques)
admin.site.register(Devis, DevisAdmin)
admin.site.register(Facture, FactureAdmin)
admin.site.register(ConseilConfiguration)

