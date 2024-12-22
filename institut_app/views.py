from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django_tenants.utils import schema_context
from .form import *
from .models import Profile

def Index(request):

    tenant = getattr(request, 'tenant', None)

    # Get the schema name or set it to "Unknown" if no tenant is found
    schema_name = tenant.schema_name if tenant else "Unknown"

    form = UserForm()
    profile = ProfilForm()

    if request.method == 'POST':
        form = UserForm(request.POST)
        profile = ProfilForm(request.POST)

        if form.is_valid() and profile.is_valid():

            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            User = get_user_model()
            User = User.objects.create_user(username=username,email = email,password=password)

            profile = Profile(user = User,adresse = 'Adresse de mon user')
            profile.save()

            return redirect('institut_app:index')


    context = {
        'schema_name' : schema_name,
        'schema_context' : schema_context,
        'form' : form,
        'profile' : profile,
    }

    return render(request, 'tenant_folder/index.html', context)


