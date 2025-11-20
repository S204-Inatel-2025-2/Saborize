from django import forms
from .models import User, TagsReceita
from django.contrib.auth.forms import UserCreationForm

class CriacaoUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class PerfilForm(forms.ModelForm):
    """Formulário para edição do perfil do usuário"""
    
    openai_api_key = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'sk-...'
        }),
        label='OpenAI API Key',
        help_text='Sua chave da API OpenAI para gerar receitas com IA. Será criptografada e armazenada com segurança.'
    )
    
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Se o usuário já tem uma API key, mostrar que ela está configurada
        if self.instance.pk and self.instance.has_openai_api_key():
            self.fields['openai_api_key'].widget.attrs['placeholder'] = 'API Key configurada - deixe em branco para manter'
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Lidar com a API key do OpenAI
        api_key = self.cleaned_data.get('openai_api_key')
        if api_key:  # Se uma nova API key foi fornecida
            user.set_openai_api_key(api_key)
        
        if commit:
            user.save()
            # Salvar as tags favoritas (many-to-many)
            self.save_m2m()
        return user