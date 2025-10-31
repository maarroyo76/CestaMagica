from django import forms
from django.contrib.auth.models import User
from .models import Producto, userProfile


# --- Formulario para Registro de Usuarios ---
class RegistroForm(forms.Form):
    username = forms.CharField(
        max_length=150, 
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Ingresa un Nombre de Usuario'})
    )
    nombre = forms.CharField(
        max_length=150, 
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Ingresa tu Nombre'})
    )
    apellido = forms.CharField(
        max_length=150, 
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Ingresa tu Apellido'})
    )
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'placeholder': 'Ingresa tu Correo'})
    )
    telefono = forms.CharField(
        max_length=8, 
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'XXXXXXXX', 'pattern': r'\d{8}'})
    )
    password = forms.CharField(
        required=True, 
        widget=forms.PasswordInput(attrs={'placeholder': 'Ingresa tu Contraseña'})
    )
    confirm_pass = forms.CharField(
        required=True, 
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirma tu Contraseña'}),
        label="Confirmar Contraseña"
    )

    # --- Validaciones automáticas ---
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("El nombre de usuario ya existe.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El correo ya está registrado.")
        return email

    def clean_confirm_pass(self):
        password = self.cleaned_data.get('password')
        confirm_pass = self.cleaned_data.get('confirm_pass')
        if password != confirm_pass:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return confirm_pass
    

# --- Formulario para Productos ---
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'stock', 'precio', 
                  'imagen', 'categoria', 'marca', 'destacado']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'destacado': forms.CheckboxInput(attrs={'role': 'switch'}),
        }
        labels = {
            'destacado': 'Marcar como destacado'
        }