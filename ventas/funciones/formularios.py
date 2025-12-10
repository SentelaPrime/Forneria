from django import forms
from django.contrib.auth.models import User
from .validators import (
    sanitizador_texto,
    validador_usuario,
    validador_correo,
    validador_contrasena_login,
    validador_contrasena_registro,
)

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Usuario o Correo Electronico",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Mjfarms o trabajador@gmail.com',
                'autocomplete': 'username',
            }
        )
    )
    password = forms.CharField(
        label="Contraseña",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Contraseña',
                'autocomplete': 'current-password',
            }
        )
    )
    
    def clean_username(self):
        """
        Este campo acepta: nombre de usuario O correo.
        1) Limpiar espacios.
        2) Si tiene '@', validar como correo.
        3) Si no, validar como usuario.
        """
        valor_original = self.cleaned_data.get('username')
        valor_limpio = sanitizador_texto(valor_original)

        if '@' in valor_limpio:
            return validador_correo(valor_limpio)
        else:
            return validador_usuario(valor_limpio)    

    def clean_password(self):
        """
        Validar contraseña para login:
        - Debe existir.
        - No espacios.
        - No '<' ni '>'.
        """
        valor_original = self.cleaned_data.get('password')
        return validador_contrasena_login(valor_original)

# --------------------------------------------------
# Formulario de registro de ususario
class RegistrationForms(forms.Form):
    username = forms.CharField(
        label="Nombre de usuario",
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mjfarms',
            'autocomplete': 'username',
        })
    )

    email = forms.EmailField(
        label="Correo electrónico",
        required=True,
        max_length=100,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'usuario@dominio.com',
            'autocomplete': 'email',
        })
    )

    password = forms.CharField(
        label="Contraseña",
        required=True,
        max_length=128,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
            'autocomplete': 'new-password',
        })
    )

    password_confirm = forms.CharField(
        label="Confirmar contraseña",
        required=True,
        max_length=128,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña',
            'autocomplete': 'new-password',
        })
    )

# ------ Metodos ----------------

    """
    clean Este es un nombre mágico para Django cuando Django valida un formulario,
    busca métodos que empiecen con clean_ seguido del nombre de un campo.
    Como nuestro campo se llama username 
    este método se ejecutará automáticamente para validar específicamente ese campo.
    """
    def clean_username(self):
        """
        Username para registro:
        - Validar formato de usuario (no correo).
        - Verificar que no exista.
        """
        username = validador_usuario(self.cleaned_data.get('username'))
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("El nombre de usuario ya existe")
        return username

    def clean_email(self):
        """
        Email para registro:
        - Validar formato.
        - Verificar que no exista.
        """
        email = validador_correo(self.cleaned_data.get('email'))
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El correo electrónico ya está registrado")
        return email

    """
    Metodo que revisa que las contraseñas sean igual
    """
    def clean(self):
        """
        Pasos
        Verificar que 'password' y 'password_confirm' coincidan.
        Aplicar reglas de fuerza a 'password' en registro.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        # Paso 1: confirmar contraseñas iguales
        if password and password_confirm and password != password_confirm:
            self.add_error("password_confirm", "Las contraseñas no coinciden")
            return cleaned_data

        # Paso 2: fortalecer contraseña (si existe)
        if password:
            cleaned_data["password"] = validador_contrasena_registro(password)

        return cleaned_data

class AdminUserEditForm(forms.ModelForm):
    password = forms.CharField(
        label="Nueva contraseña",
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Dejar vacío para no cambiar',
            'autocomplete': 'new-password',
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_username(self):
        username = validador_usuario(self.cleaned_data.get('username'))
        existe = User.objects.filter(username=username).exclude(pk=self.instance.pk).exists()
        if existe:
            raise forms.ValidationError("El nombre de usuario ya existe")
        return username

    def clean_email(self):
        email = validador_correo(self.cleaned_data.get('email'))
        existe = User.objects.filter(email=email).exclude(pk=self.instance.pk).exists()
        if existe:
            raise forms.ValidationError("El correo electrónico ya está registrado")
        return email

    def clean_first_name(self):
        valor = sanitizador_texto(self.cleaned_data.get('first_name') or '')
        return valor

    def clean_last_name(self):
        valor = sanitizador_texto(self.cleaned_data.get('last_name') or '')
        return valor

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        if pwd:
            return validador_contrasena_registro(pwd)
        return pwd
