from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from ..models import DepensesCategory

@login_required(login_url="institut_app:login")
def ApiLoadDepensesCategories(request):
    """
    Returns a list of all categories. 
    You might want to return them as a tree or just a flat list with parent_id.
    Here, a flat list with parent info is versatile enough for JS tree building or select boxes.
    """
    if request.method == 'GET':
        categories = DepensesCategory.objects.all().order_by('name')
        data = []
        for cat in categories:
            data.append({
                'id': cat.id,
                'name': cat.name,
                'parent_id': cat.parent.id if cat.parent else None,
                'parent_name': cat.parent.name if cat.parent else None,
                'created_at': cat.created_at.strftime('%Y-%m-%d') if cat.created_at else '-',
                'updated_at': cat.updated_at.strftime('%Y-%m-%d') if cat.updated_at else '-',
            })
        return JsonResponse(data, safe=False)
    return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiStoreDepenseCategory(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        parent_id = request.POST.get('parent_id')
        
        parent = None
        if parent_id:
            try:
                parent = DepensesCategory.objects.get(id=parent_id)
            except DepensesCategory.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Parent category not found"})

        try:
            category = DepensesCategory.objects.create(name=name, parent=parent)
            return JsonResponse({
                "status": "success", 
                "message": "Category created successfully",
                "category": {
                    "id": category.id,
                    "name": category.name,
                    "parent_id": category.parent.id if category.parent else None
                }
            })
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
            
    return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiUpdateDepenseCategory(request):
    if request.method == 'POST':
        cat_id = request.POST.get('id')
        name = request.POST.get('name')
        parent_id = request.POST.get('parent_id') # Can be empty/None to remove parent

        try:
            category = DepensesCategory.objects.get(id=cat_id)
            category.name = name
            
            if parent_id:
                try:
                    parent = DepensesCategory.objects.get(id=parent_id)
                    # Simple cycle check: prevent self-parenting
                    if parent.id == category.id:
                         return JsonResponse({"status": "error", "message": "Cannot be your own parent"})
                    category.parent = parent
                except DepensesCategory.DoesNotExist:
                    return JsonResponse({"status": "error", "message": "Parent category not found"})
            else:
                 category.parent = None
            
            category.save()
            return JsonResponse({"status": "success", "message": "Category updated successfully"})
        except DepensesCategory.DoesNotExist:
             return JsonResponse({"status": "error", "message": "Category not found"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiDeleteDepenseCategory(request):
     if request.method == 'GET':
        cat_id = request.GET.get('id')
        try:
            category = DepensesCategory.objects.get(id=cat_id)
            category.delete()
            return JsonResponse({"status": "success", "message": "Category deleted successfully"})
        except DepensesCategory.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Category not found"})
     return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)
