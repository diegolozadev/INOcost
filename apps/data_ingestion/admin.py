from django.contrib import admin
from .models import TipoCosto, DetalleMovimientosContables

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


# --- REGISTRO DE MOVIMIENTOS CONTABLES  ---
@admin.register(DetalleMovimientosContables)
class DetalleMovimientosAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'auxiliar', 'razon_social', 'debito', 'credito', 'neto', 'unidad_negocio_codigo')
    list_filter = ('fecha', 'desc_unidad_negocio')
    
    # Esto asegura que Django siempre intente contar todo
    show_full_result_count = True 
    list_per_page = 100

    def changelist_view(self, request, extra_context=None):
        # 1. Obtenemos el total de la base de datos
        total = DetalleMovimientosContables.objects.count()
        
        # 2. Inyectamos el número en el título de la página
        extra_context = extra_context or {}
        extra_context['title'] = f"Movimientos Cargados: {total} registros"
        
        return super().changelist_view(request, extra_context=extra_context)

    # Hacer que los montos sean de solo lectura si prefieres que no se editen manualmente
    # readonly_fields = ('neto',)