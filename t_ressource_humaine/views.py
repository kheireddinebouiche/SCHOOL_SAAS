from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DetailView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Contrat, FichePaie, ParametresPaie
from .logic import PaieEngine
from django import forms
from decimal import Decimal
from t_formations.models import Formateurs
from institut_app.models import Entreprise

class ContratListView(LoginRequiredMixin, ListView):
    model = Contrat
    context_object_name = 'contrats'

    def get_queryset(self):
        active_id = self.request.session.get('active_entreprise_id')
        if active_id == 'none':
            return super().get_queryset().filter(entreprise__isnull=True)
        if active_id:
            return super().get_queryset().filter(entreprise_id=active_id)
        return super().get_queryset().none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entreprises'] = Entreprise.objects.all()
        context['active_entreprise_id'] = self.request.session.get('active_entreprise_id')
        return context

class ContratForm(forms.ModelForm):
    class Meta:
        model = Contrat
        fields = '__all__'
        widgets = {
            'formateur': forms.Select(attrs={'class': 'form-select'}),
            'type_contrat': forms.Select(attrs={'class': 'form-select'}),
            'date_debut': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'salaire_base': forms.NumberInput(attrs={'class': 'form-control'}),
            'salaire_horaire': forms.NumberInput(attrs={'class': 'form-control'}),
            'prime_transport': forms.NumberInput(attrs={'class': 'form-control'}),
            'prime_panier': forms.NumberInput(attrs={'class': 'form-control'}),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

from django.http import JsonResponse
from django.template.loader import render_to_string

class ContratCreateView(LoginRequiredMixin, CreateView):
    model = Contrat
    form_class = ContratForm
    template_name = 't_ressource_humaine/contrat_form.html'
    success_url = reverse_lazy('t_ressource_humaine:contrat_list')

    def get_template_names(self):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return ['t_ressource_humaine/_contrat_form.html']
        return [self.template_name]

    def form_valid(self, form):
        active_id = self.request.session.get('active_entreprise_id')
        if not active_id:
             return JsonResponse({'status': 'error', 'message': 'Veuillez sélectionner une entreprise avant de créer un contrat'})
        
        # Convert 'none' string to None for the database
        form.instance.entreprise_id = active_id if active_id != 'none' else None
        
        self.object = form.save()
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Contrat créé avec succès'})
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string(
                't_ressource_humaine/_contrat_form.html',
                {'form': form},
                request=self.request
            )
            return JsonResponse({'status': 'invalid', 'html': html})
        return super().form_invalid(form)

class ContratUpdateView(LoginRequiredMixin, UpdateView):
    model = Contrat
    form_class = ContratForm
    template_name = 't_ressource_humaine/contrat_form.html'
    success_url = reverse_lazy('t_ressource_humaine:contrat_list')

    def get_template_names(self):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return ['t_ressource_humaine/_contrat_form.html']
        return [self.template_name]

    def form_valid(self, form):
        self.object = form.save()
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Contrat modifié avec succès'})
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string(
                't_ressource_humaine/_contrat_form.html',
                {'form': form},
                request=self.request
            )
            return JsonResponse({'status': 'invalid', 'html': html})
        return super().form_invalid(form)

class ContratDetailView(LoginRequiredMixin, DetailView):
    model = Contrat
    template_name = 't_ressource_humaine/contrat_print.html'

# -- Paie --

class FichePaieGenerationForm(forms.Form):
    mois = forms.ChoiceField(choices=FichePaie.MOIS_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    annee = forms.IntegerField(initial=2024, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    jours_travailles = forms.IntegerField(initial=22, min_value=0, max_value=31, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    heures_travailles = forms.DecimalField(initial=0, min_value=0, required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    primes_exceptionnelles = forms.DecimalField(initial=0, required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    retenues_absences = forms.DecimalField(initial=0, required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    avance_sur_salaire = forms.DecimalField(initial=0, required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))


def generer_paie(request, contrat_id):
    contrat = get_object_or_404(Contrat, pk=contrat_id)
    
    if request.method == 'POST':
        form = FichePaieGenerationForm(request.POST)
        if form.is_valid():
            mois = int(form.cleaned_data['mois'])
            annee = form.cleaned_data['annee']
            jours = form.cleaned_data['jours_travailles']
            heures = form.cleaned_data['heures_travailles'] or 0
            primes_ex = form.cleaned_data.get('primes_exceptionnelles') or 0
            retenues = form.cleaned_data.get('retenues_absences') or 0
            avance = form.cleaned_data.get('avance_sur_salaire') or 0
            
            if FichePaie.objects.filter(contrat=contrat, mois=mois, annee=annee).exists():
                message = f"Une fiche de paie existe déjà pour {mois}/{annee}"
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'error', 'message': message})
                messages.error(request, message)
                return redirect('t_ressource_humaine:contrat_list')
            
            result = PaieEngine.calculer_paie(contrat, jours, heures)
            
            # Note: PaieEngine currently doesn't factor in primes_exceptionnelles etc. in its net calculation.
            # I should either update PaieEngine or calculate the final net here.
            # For simplicity, I will save them and use PaieEngine result as starting point.
            
            final_net = result['net_a_payer'] + Decimal(primes_ex) - Decimal(retenues) - Decimal(avance)

            fiche = FichePaie(
                contrat=contrat,
                entreprise=contrat.entreprise,
                mois=mois,
                annee=annee,
                jours_travailles=jours,
                heures_travailles=heures,
                primes_exceptionnelles=primes_ex,
                retenues_absences=retenues,
                avance_sur_salaire=avance,
                salaire_base_calcule=result['salaire_base_calcule'],
                base_ss=result['base_ss'],
                montant_ss=result['montant_ss'],
                salaire_imposable=result['salaire_imposable'],
                irg=result['irg'],
                net_a_payer=final_net,
                prime_panier=result['prime_panier'],
                prime_transport=result['prime_transport']
            )
            if contrat.entreprise:
                fiche.entreprise = contrat.entreprise
            fiche.save()
            
            msg = f"Fiche de paie générée : Net {fiche.net_a_payer} DA"
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success', 
                    'message': msg,
                    'show_modal': True,
                    'redirect_url': reverse_lazy('t_ressource_humaine:fiche_paie_detail', kwargs={'pk': fiche.pk})
                })
            messages.success(request, msg)
            return redirect('t_ressource_humaine:fiche_paie_detail', pk=fiche.pk)
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                html = render_to_string(
                    't_ressource_humaine/_generate_paie_form.html',
                    {'form': form, 'contrat': contrat},
                    request=request
                )
                return JsonResponse({'status': 'invalid', 'html': html})
    else:
        # Load config to get default working days
        config = ParametresPaie.get_config(entreprise=contrat.entreprise)
        form = FichePaieGenerationForm(initial={
            'jours_travailles': config.jours_travailles_standard,
            'annee': 2024 # Or use current year
        })
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 't_ressource_humaine/_generate_paie_form.html', {'form': form, 'contrat': contrat})
        
    return render(request, 't_ressource_humaine/generate_paie.html', {'form': form, 'contrat': contrat})

class FichePaieDetailView(LoginRequiredMixin, DetailView):
    model = FichePaie
    template_name = 't_ressource_humaine/fiche_paie_print.html'
    context_object_name = 'fiche'

    def get_template_names(self):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return ['t_ressource_humaine/_fiche_paie_detail.html']
        return [self.template_name]

class FichePaieListView(LoginRequiredMixin, ListView):
    model = FichePaie
    template_name = 't_ressource_humaine/fiche_paie_list.html'
    context_object_name = 'fiches'

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            self.object_list = self.get_queryset()
            context = self.get_context_data()
            return render(request, 't_ressource_humaine/_fiche_paie_table.html', context)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        active_id = self.request.session.get('active_entreprise_id')
        queryset = super().get_queryset().select_related('contrat__formateur').order_by('-annee', '-mois', '-generated_at')
        
        if active_id == 'none':
            queryset = queryset.filter(entreprise__isnull=True)
        elif active_id:
            queryset = queryset.filter(entreprise_id=active_id)
        else:
            queryset = queryset.none()
        contrat_id = self.request.GET.get('contrat')
        formateur_id = self.request.GET.get('formateur')
        annee = self.request.GET.get('annee')
        
        if contrat_id:
            queryset = queryset.filter(contrat_id=contrat_id)
        if formateur_id:
            queryset = queryset.filter(contrat__formateur_id=formateur_id)
        if annee:
            queryset = queryset.filter(annee=annee)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entreprises'] = Entreprise.objects.all()
        context['active_entreprise_id'] = self.request.session.get('active_entreprise_id')
        
        contrat_id = self.request.GET.get('contrat')
        formateur_id = self.request.GET.get('formateur')
        annee_selected = self.request.GET.get('annee')
        
        if contrat_id:
            context['filter_contrat'] = get_object_or_404(Contrat, pk=contrat_id)
        
        context['formateurs'] = Formateurs.objects.all().order_by('nom')
        context['selected_formateur'] = int(formateur_id) if formateur_id and formateur_id.isdigit() else None
        context['selected_annee'] = int(annee_selected) if annee_selected and annee_selected.isdigit() else None
        
        # Get unique years from FichePaie for the year filter
        context['years'] = FichePaie.objects.values_list('annee', flat=True).distinct().order_by('-annee')
        
        return context

class ParametresPaieForm(forms.ModelForm):
    class Meta:
        model = ParametresPaie
        fields = ['taux_ss', 'jours_travailles_standard', 'seuil_exoneration_irg']
        widgets = {
            'taux_ss': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001'}),
            'jours_travailles_standard': forms.NumberInput(attrs={'class': 'form-control'}),
            'seuil_exoneration_irg': forms.NumberInput(attrs={'class': 'form-control'}),
        }

def config_paie(request):
    active_id = request.session.get('active_entreprise_id')
    if not active_id:
        messages.warning(request, "Veuillez sélectionner une entreprise ou 'Non-affectés' pour accéder à la configuration.")
        return redirect('t_ressource_humaine:contrat_list')
        
    if active_id == 'none':
        entreprise = None
    else:
        entreprise = get_object_or_404(Entreprise, pk=active_id)
        
    config = ParametresPaie.get_config(entreprise=entreprise)
    if request.method == 'POST':
        form = ParametresPaieForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, "Configuration de la paie mise à jour")
            return redirect('t_ressource_humaine:config_paie')
    else:
        form = ParametresPaieForm(instance=config)
    
    return render(request, 't_ressource_humaine/parametres_paie.html', {'form': form, 'config': config})

def select_entreprise_paie(request):
    if request.method == 'POST':
        entreprise_id = request.POST.get('entreprise_id')
        request.session['active_entreprise_id'] = entreprise_id
        if entreprise_id == 'none':
            messages.info(request, "Affichage des données non-affectées.")
        elif entreprise_id:
            messages.success(request, f"Entreprise sélectionnée avec succès.")
        else:
            messages.warning(request, "Aucune entreprise sélectionnée.")
        return redirect(request.META.get('HTTP_REFERER', 't_ressource_humaine:contrat_list'))
    return redirect('t_ressource_humaine:contrat_list')
