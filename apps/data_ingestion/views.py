from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import TipoCosto

# 1. LISTAR TODOS LOS COSTOS
class TipoCostoListView(ListView):
    model = TipoCosto
    template_name = 'costos/tipocosto_list.html'
    context_object_name = 'costos'
    # Ordenamos por fecha de creación o ID (puedes agregar un campo 'creado_en' a tu modelo)
    ordering = ['-id']