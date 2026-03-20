from django.contrib import admin
from .models import TipoCosto

@admin.register(TipoCosto)
class TipoCostoAdmin(admin.ModelAdmin):
    # Columnas que se verán en la tabla principal
    list_display = (
        'cuenta_auxiliar', 
        'tipo_costo', 
        'detalle_costo', 
        'registrado_por',
    )
    
    # Filtros laterales (muy útiles para auditoría clínica)
    list_filter = ('tipo_costo', 'registrado_por')
    
    # Buscador por cuenta o detalle
    search_fields = ('cuenta_auxiliar', 'detalle_costo')
    
    # Organización de campos dentro del formulario de edición
    fieldsets = (
        ('Información Contable', {
            'fields': ('cuenta_auxiliar', 'tipo_costo', 'detalle_costo')
        }),
        ('Auditoría', {
            'fields': ('registrado_por',),
            'classes': ('collapse',), # Esto lo oculta por defecto
        }),
    )

    def save_model(self, request, obj, form, change):
        """
        Al igual que en la vista, si creamos el registro desde el admin,
        asignamos automáticamente al usuario logueado.
        """
        if not obj.registrado_por:
            obj.registrado_por = request.user
        super().save_model(request, obj, form, change)