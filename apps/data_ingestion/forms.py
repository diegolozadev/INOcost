from django import forms

class ImportarMovimientosForm(forms.Form):
    archivo = forms.FileField(
        label="Selecciona el archivo (CSV o Excel)",
        help_text="Asegúrate de que las columnas coincidan con el modelo."
    )