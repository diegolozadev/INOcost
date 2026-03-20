from django.urls import path
from . import views

urlpatterns = [
    path('list_cost/', views.TipoCostoListView.as_view(), name='lista_costos'),
]
