from django.db import models
from django.conf import settings

# Create your models here.

class TipoCosto(models.Model):
    
    TIPO_COSTOS = [
        ("INGRESO", "INGRESO"),
        ("GASTO", "GASTO"),
        ("COSTO_VENTA", "COSTO VENTA"),
        ("INSUMOS", "INSUMOS"),
        ("MANO_OBRA", "MANO OBRA"),
        ("CIF", "CIF"),
    ]
    
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
        )
    
    # Relación con el modelo User
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    
    cuenta_auxiliar = models.CharField(max_length=8)
    tipo_costo = models.CharField(max_length=20, choices=TIPO_COSTOS)
    detalle_costo = models.CharField(max_length=50, choices=CHOICES_CONTABLES)
    