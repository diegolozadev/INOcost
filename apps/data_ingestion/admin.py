from django.contrib import admin
from django.contrib.auth import get_user_model
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from .models import TipoCosto, DetalleMovimientosContables

User = get_user_model()

# --- RECURSO PARA TIPO DE COSTO ---
class TipoCostoResource(resources.ModelResource):
    registrado_por = fields.Field(
        column_name='registrado_por',
        attribute='registrado_por',
        widget=ForeignKeyWidget(User, 'username')
    )

    class Meta:
        model = TipoCosto
        fields = ('id', 'cuenta_auxiliar', 'tipo_costo', 'detalle_costo', 'registrado_por')
        import_id_fields = ['cuenta_auxiliar']

@admin.register(TipoCosto)
class TipoCostoAdmin(ImportExportModelAdmin):
    resource_class = TipoCostoResource
    # Usamos get_detalle_costo_display para que en la lista del admin se vea el texto amigable
    list_display = ('cuenta_auxiliar', 'tipo_costo', 'mostrar_detalle', 'registrado_por')
    list_filter = ('tipo_costo', 'registrado_por')
    search_fields = ('cuenta_auxiliar', 'detalle_costo')

    def mostrar_detalle(self, obj):
        return obj.get_detalle_costo_display()
    mostrar_detalle.short_description = 'Detalle de Costo'


# --- RECURSO PARA MOVIMIENTOS CONTABLES ---
class DetalleMovimientosResource(resources.ModelResource):
    class Meta:
        model = DetalleMovimientosContables
        fields = (
            'clase', 'fecha', 'auxiliar', 'desc_auxiliar', 
            'c_o_mvto', 'desc_c_o_mvto', 'unidad_negocio_codigo', 
            'desc_unidad_negocio', 'docto_proveedor', 'tercero_mvto', 
            'razon_social', 'debito', 'credito', 'neto'
        )

@admin.register(DetalleMovimientosContables)
class DetalleMovimientosAdmin(ImportExportModelAdmin):
    resource_class = DetalleMovimientosResource
    # Agregamos los métodos personalizados a la lista
    list_display = (
        'fecha', 
        'auxiliar', 
        'razon_social', 
        'get_tipo_costo',    # Columna nueva
        'get_detalle_costo', # Columna nueva
        'neto'
    )
    list_filter = ('fecha', 'mapeo_costo__tipo_costo') # Filtro por el tipo de costo relacionado
    search_fields = ('auxiliar', 'razon_social')
    list_select_related = ('mapeo_costo',) # INDISPENSABLE para velocidad
    list_per_page = 100

    # --- MÉTODOS PARA MOSTRAR LA RELACIÓN ---
    
    def get_tipo_costo(self, obj):
        if obj.mapeo_costo:
            return obj.mapeo_costo.tipo_costo
        return "-"
    get_tipo_costo.short_description = 'Tipo'
    get_tipo_costo.admin_order_field = 'mapeo_costo__tipo_costo'

    def get_detalle_costo(self, obj):
        if obj.mapeo_costo:
            # Aquí es donde ocurre la magia del "display"
            return obj.mapeo_costo.get_detalle_costo_display()
        return "Pendiente"
    get_detalle_costo.short_description = 'Detalle Costo'

    def changelist_view(self, request, extra_context=None):
        total = DetalleMovimientosContables.objects.count()
        extra_context = extra_context or {}
        extra_context['title'] = f"Auditoría: {total} registros cargados"
        return super().changelist_view(request, extra_context=extra_context)