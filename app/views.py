from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def Index(request):
    tenant = getattr(request, 'tenant', None)

    # Get the schema name or set it to "Unknown" if no tenant is found
    schema_name = tenant.schema_name if tenant else "Unknown"

    return HttpResponse(f"<h4>Bienvenue sur votre site public {schema_name}</h4>")