from django.db import models
from django.conf import settings

# Create your models here.

class TipoCosto(models.Model):
    
    # TIPO_COSTOS = [
    #     ("INGRESO", "INGRESO"),
    #     ("GASTO", "GASTO"),
    #     ("COSTO_VENTA", "COSTO VENTA"),
    #     ("INSUMOS", "INSUMOS"),
    #     ("MANO_OBRA", "MANO OBRA"),
    #     ("CIF", "CIF"),
    # ]
    
    CHOICES_CONTABLES = (
            ('INGRESO', 'INGRESO'),
            ('GASTO', 'GASTO'),
            ('COSTO_VENTA', 'COSTO DE VENTA'),
            ('INSUMOS', 'INSUMOS'),
            ('MANO_OBRA', 'MANO DE OBRA'),
            ('CIF_OTROS_CIF', 'CIF OTROS CIF'),
            ('CIF_HONORARIOS', 'CIF OTROS HONORARIOS'),
            ('CIF_ARRENDAMIENTO', 'CIF ARRENDAMIENTO'),
            ('CIF_ALQUILER_EQUIPO', 'CIF ALQUILER EQUIPO MEDICO'),
            ('CIF_ARREN_OTROS', 'CIF ARREN. OTROS ACTIVOS'),
            ('CIF_SERV_PUBLICOS', 'CIF SERVICIOS PUBLICOS'),
            ('CIF_TRANSPORTE', 'CIF TRANSPORTE Y ALOJAMIENTO'),
            ('CIF_OTROS_SERV', 'CIF OTROS SERVICIOS'),
            ('CIF_SALA', 'CIF DERECHOS DE SALA'),
            ('CIF_ANESTESIA', 'CIF ANESTESIOLOGIA'),
            ('CIF_PATOLOGIA', 'CIF PATOLOGIA'),
            ('OXIGENO', 'OXIGENO'),
            ('CILINDRO_MEZCLA', 'CILINDRO MEZCLA DE DIFUSIÓN'),
            ('CIF_MED_INSUMOS', 'CIF MEDICAMENTOS E INSUMOS (PROCEDIMIENTOS)'),
            ('CIF_MANTENIMIENTO', 'CIF MANTENIMIENTO'),
            ('CIF_DEPRECIACION', 'CIF DEPRECIACION'),
            ('CIF_COPAGOS', 'CIF COPAGOS ASUMIDOS'),
            ('CIF_ASEO_CAFE', 'OTROS CIF ELEMENTOS DE ASEO Y CAFETERIA'),
            ('CIF_PAPELERIA', 'OTROS CIF UTILES, PAPELERIA Y FOTOCOPIAS'),
            ('CIF_TRANSPORTE_EQUIPO_MEDICO', 'CIF TRANSPORTE EQUIPO MÉDICO'),
            ('CELULARES', 'CELULARES'),
        )
    
    # Relación con el modelo User
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    
    cuenta_auxiliar = models.CharField(max_length=8)
    tipo_costo = models.CharField(max_length=20)
    detalle_costo = models.CharField(max_length=50, choices=CHOICES_CONTABLES)
    
    
    def nombre_detalle(self):
        return self.get_detalle_costo_display()
    
class DetalleMovimientosContables(models.Model):
    clase = models.CharField(max_length=100)
    fecha = models.DateField()
    auxiliar = models.CharField(max_length=8)
    desc_auxiliar = models.CharField(max_length=100)
    
    # NUEVA RELACIÓN:
    # Vincula el movimiento con su clasificación de costo basada en el auxiliar
    mapeo_costo = models.ForeignKey(
        TipoCosto, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='movimientos'
    )
    
    
    c_o_mvto = models.CharField(max_length=100, verbose_name="C.O. Movimiento")
    desc_c_o_mvto = models.CharField(max_length=100, verbose_name="Descripción C.O.")
    unidad_negocio_codigo = models.CharField(max_length=4)
    docto_proveedor = models.CharField(max_length=100)
    desc_unidad_negocio = models.CharField(max_length=100)
    tercero_mvto = models.CharField(max_length=100)
    razon_social = models.CharField(max_length=100)
    
    # Campos Financieros (Corregidos con precisión)
    debito = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    credito = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    neto = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    tipo_doc_contable = models.CharField(max_length=100)
    grupo_contable = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Detalle de Movimiento Contable"
        verbose_name_plural = "Detalles de Movimientos Contables"
        ordering = ['-fecha', 'auxiliar']

    def __str__(self):
        return f"{self.fecha} - {self.auxiliar} - {self.razon_social} (${self.neto})"