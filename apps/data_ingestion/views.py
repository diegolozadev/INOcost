from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import TipoCosto, DetalleMovimientosContables
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ImportarMovimientosForm
import pandas as pd


# 1. LISTAR TODOS LOS COSTOS
class TipoCostoListView(ListView):
    model = TipoCosto
    template_name = 'costos/tipocosto_list.html'
    context_object_name = 'costos'
    # Ordenamos por fecha de creación o ID (puedes agregar un campo 'creado_en' a tu modelo)
    ordering = ['-id']
    
# VISTA para cargar excel de movimiento contables de siesa
def importar_movimientos_view(request):
    if request.method == 'POST':
        form = ImportarMovimientosForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']
            
            try:
                # 1. Leer según la extensión
                if archivo.name.endswith('.csv'):
                    df = pd.read_csv(archivo)
                else:
                    df = pd.read_excel(archivo)

                # 2. NORMALIZACIÓN: Convertir encabezados a minúsculas y quitar espacios
                # Esto evita errores si el Excel dice "FECHA" en vez de "fecha"
                df.columns = [str(c).strip().lower() for c in df.columns]

                # 3. LIMPIEZA DE DATOS
                # Convertir fechas de Excel a formato Python date
                if 'fecha' in df.columns:
                    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce').dt.date
                
                # Rellenar nulos y asegurar tipos numéricos
                df['debito'] = pd.to_numeric(df.get('debito', 0), errors='coerce').fillna(0)
                df['credito'] = pd.to_numeric(df.get('credito', 0), errors='coerce').fillna(0)
                df['neto'] = df['debito'] - df['credito']

                # Eliminar filas donde la fecha sea nula (filas vacías al final del Excel)
                df = df.dropna(subset=['fecha'])

                movimientos_a_crear = []
                
                for index, row in df.iterrows():
                    # Usamos .get() para evitar KeyError si falta una columna opcional
                    obj = DetalleMovimientosContables(
                        clase=str(row.get('clase', '')),
                        fecha=row['fecha'],
                        auxiliar=str(row.get('auxiliar', ''))[:8], # Truncar a max_length
                        desc_auxiliar=str(row.get('desc_auxiliar', '')),
                        c_o_mvto=str(row.get('c_o_mvto', '')),
                        desc_c_o_mvto=str(row.get('desc_c_o_mvto', '')),
                        unidad_negocio_codigo=str(row.get('unidad_negocio_codigo', ''))[:4],
                        desc_unidad_negocio=str(row.get('desc_unidad_negocio', '')),
                        docto_proveedor=str(row.get('docto_proveedor', '')),
                        tercero_mvto=str(row.get('tercero_mvto', '')),
                        razon_social=str(row.get('razon_social', '')),
                        debito=row['debito'],
                        credito=row['credito'],
                        neto=row['neto'],
                        tipo_doc_contable=str(row.get('tipo_doc_contable', '')),
                        grupo_contable=str(row.get('grupo_contable', '')), # Corregido typo 'groupo'
                    )
                    movimientos_a_crear.append(obj)

                # 4. GUARDADO MASIVO
                if movimientos_a_crear:
                    DetalleMovimientosContables.objects.bulk_create(movimientos_a_crear)
                    messages.success(request, f"¡Éxito! Se importaron {len(movimientos_a_crear)} registros.")
                else:
                    messages.warning(request, "No se encontraron datos válidos para importar.")
                
                return redirect('data_ingestion/lista_movimientos.html')

            except Exception as e:
                messages.error(request, f"Error crítico al procesar el archivo: {e}")
                # Imprimir el error en consola para debug
                print(f"DEBUG ERROR: {e}")
    else:
        form = ImportarMovimientosForm()
    
    # Asegúrate de que el path del template sea el correcto en tu estructura de carpetas
    return render(request, 'data_ingestion/importar_movimientos.html', {'form': form})


class MovimientosListView(LoginRequiredMixin, ListView):
    model = DetalleMovimientosContables
    template_name = 'data_ingestion/lista_movimientos.html'
    context_object_name = 'movimientos'
    # Definimos cuántos registros ver por página (ej. 100 es ideal para contabilidad)
    paginate_by = 200
    ordering = ['-fecha', '-id']

    def get_queryset(self):
        # Aquí puedes optimizar la consulta para que no traiga campos innecesarios si la tabla es gigante
        return super().get_queryset().select_related()