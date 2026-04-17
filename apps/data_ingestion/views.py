import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.generic import ListView
from .models import TipoCosto, DetalleMovimientosContables
from .forms import ImportarMovimientosForm

# 1. LISTAR TIPO DE COSTOS
class TipoCostoListView(ListView):
    model = TipoCosto
    template_name = 'costos/tipocosto_list.html'
    context_object_name = 'costos'
    ordering = ['-id']

# 2. VISTA DE IMPORTACIÓN (SIESA)
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

                # 2. NORMALIZACIÓN DE ENCABEZADOS
                df.columns = [str(c).strip().lower() for c in df.columns]

                # 3. LIMPIEZA DE DATOS FINANCIEROS Y FECHAS
                if 'fecha' in df.columns:
                    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce').dt.date
                
                # Asegurar que las columnas existan antes de operar
                df['debito'] = pd.to_numeric(df.get('debito', 0), errors='coerce').fillna(0)
                df['credito'] = pd.to_numeric(df.get('credito', 0), errors='coerce').fillna(0)
                df['neto'] = df['debito'] - df['credito']
                
                # Quitar filas sin fecha (evita errores en bulk_create)
                df = df.dropna(subset=['fecha'])

                # --- LÓGICA DE MAPEO (OPTIMIZADA) ---
                # Traemos el catálogo de TipoCosto a memoria
                dict_mapeo = {str(tc.cuenta_auxiliar).strip(): tc for tc in TipoCosto.objects.all()}
                
                movimientos_a_crear = []
                
                for _, row in df.iterrows():
                    # Limpiamos el auxiliar del Excel para que coincida con la DB
                    auxiliar_excel = str(row.get('auxiliar', '')).strip()[:8]
                    
                    # Buscamos la relación
                    costo_relacionado = dict_mapeo.get(auxiliar_excel)

                    obj = DetalleMovimientosContables(
                        clase=str(row.get('clase', '')).strip(),
                        fecha=row['fecha'],
                        auxiliar=auxiliar_excel,
                        desc_auxiliar=str(row.get('desc_auxiliar', '')).strip(),
                        c_o_mvto=str(row.get('c_o_mvto', '')).strip(),
                        desc_c_o_mvto=str(row.get('desc_c_o_mvto', '')).strip(),
                        unidad_negocio_codigo=str(row.get('unidad_negocio_codigo', '')).strip()[:4],
                        docto_proveedor=str(row.get('docto_proveedor', '')).strip(),
                        desc_unidad_negocio=str(row.get('desc_unidad_negocio', '')).strip(),
                        tercero_mvto=str(row.get('tercero_mvto', '')).strip(),
                        razon_social=str(row.get('razon_social', '')).strip(),
                        debito=row['debito'],
                        credito=row['credito'],
                        neto=row['neto'],
                        tipo_doc_contable=str(row.get('tipo_doc_contable', '')).strip(),
                        grupo_contable=str(row.get('grupo_contable', '')).strip(),
                        mapeo_costo=costo_relacionado
                    )
                    movimientos_a_crear.append(obj)

                # 4. GUARDADO MASIVO
                if movimientos_a_crear:
                    DetalleMovimientosContables.objects.bulk_create(movimientos_a_crear, batch_size=1000)
                    messages.success(request, f"Se importaron {len(movimientos_a_crear)} movimientos exitosamente.")
                else:
                    messages.warning(request, "El archivo no contenía datos válidos.")
                
                return redirect('lista_movimientos')

            except Exception as e:
                messages.error(request, f"Error al procesar el Excel: {e}")
    else:
        form = ImportarMovimientosForm()
    
    return render(request, 'data_ingestion/importar_movimientos.html', {'form': form})

# 3. LISTADO DE MOVIMIENTOS (AUDITORÍA)
def lista_movimientos_view(request):
    # select_related('mapeo_costo') es lo que permite que el template 
    # vea la descripción del TipoCosto sin fallar
    queryset = DetalleMovimientosContables.objects.select_related('mapeo_costo').all().order_by('-fecha', 'auxiliar')
    
    paginator = Paginator(queryset, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'data_ingestion/lista_movimientos.html', {
        'movimientos': page_obj,
        'page_obj': page_obj,
        'paginator': paginator,
        'is_paginated': page_obj.has_other_pages(),
    })