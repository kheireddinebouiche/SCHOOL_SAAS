from django.contrib import admin
from .models import PaymentCategory

@admin.register(PaymentCategory)
class PaymentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'category_type', 'created_at')
    list_filter = ('category_type',)
    search_fields = ('name',)
