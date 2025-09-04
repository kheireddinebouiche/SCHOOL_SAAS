from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime

# Modèles (à adapter selon votre structure de données)
# from .models import Derogation

@login_required
def liste_derogations(request):
    """
    Vue pour afficher la liste des dérogations.
    """
    context = {
        'page_title': 'Liste des dérogations',
    }
    return render(request, 'tenant_folder/crm/liste_derogations.html', context)

# Si vous avez un modèle Derogation, vous pouvez utiliser une vue basée sur les classes comme celle-ci :
"""
@method_decorator(login_required, name='dispatch')
class ListeDerogationsView(ListView):
    model = Derogation
    template_name = 'tenant_folder/crm/liste_derogations.html'
    context_object_name = 'derogations'
    paginate_by = 20
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Liste des dérogations'
        return context
        
    def get_queryset(self):
        queryset = super().get_queryset()
        # Ajouter des filtres si nécessaire
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(demandeur__icontains=search) |
                Q(type__icontains=search) |
                Q(motif__icontains=search)
            )
        return queryset
"""