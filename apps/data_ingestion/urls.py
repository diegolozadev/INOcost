from django.urls import path
from . import views

urlpatterns = [
    path('list_cost/', views.TipoCostoListView.as_view(), name='lista_costos'),
    path('load_movt/', views.importar_movimientos_view, name="cargar_movimientos"),
    path('list_movt/', views.lista_movimientos_view, name='lista_movimientos'),
    path('reporte_dinamico/', views.matriz_costos_view, name='reporte_dinamico'),
]
