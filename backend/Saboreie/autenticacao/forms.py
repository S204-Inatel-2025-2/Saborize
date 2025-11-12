from django import forms
from .models import User, TagsReceita
from django.contrib.auth.forms import UserCreationForm

class CriacaoUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class PerfilForm(forms.ModelForm):
    """Formulário para edição do perfil do usuário"""
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'bio', 'telefone', 
            'data_nascimento', 'cidade', 'estado', 'foto_perfil', 'tags_favoritas'
        ]
        
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Seu primeiro nome'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Seu sobrenome'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'seu@email.com'
            }),
            'bio': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Conte um pouco sobre você...'
            }),
            'telefone': forms.TextInput(attrs={
                'placeholder': '(11) 99999-9999'
            }),
            'data_nascimento': forms.DateInput(attrs={
                'type': 'date'
            }),
            'cidade': forms.TextInput(attrs={
                'placeholder': 'Sua cidade'
            }),
            'estado': forms.TextInput(attrs={
                'placeholder': 'Seu estado'
            }),
            'foto_perfil': forms.FileInput(attrs={
                'accept': 'image/*'
            }),
            'tags_favoritas': forms.CheckboxSelectMultiple(),
        }
        
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
            'bio': 'Biografia',
            'telefone': 'Telefone',
            'data_nascimento': 'Data de Nascimento',
            'cidade': 'Cidade',
            'estado': 'Estado',
            'foto_perfil': 'Foto de Perfil',
            'tags_favoritas': 'Tipos de Receitas Favoritas'
        }
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Este e-mail já está sendo usado por outro usuário.')
        return email