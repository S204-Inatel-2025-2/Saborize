from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, TagsReceita

# Register your models here.

@admin.register(TagsReceita)
class TagsReceitaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'criada_em')
    search_fields = ('nome', 'descricao')
    ordering = ('nome',)
    
    def save_model(self, request, obj, form, change):
        # Converte para lowercase para evitar duplicatas
        obj.nome = obj.nome.lower().strip()
        super().save_model(request, obj, form, change)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Adiciona os campos customizados à interface do admin
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informações Adicionais', {
            'fields': ('bio', 'foto_perfil', 'telefone', 'data_nascimento', 
                      'cidade', 'estado', 'tags_favoritas')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Informações Adicionais', {
            'fields': ('bio', 'foto_perfil', 'telefone', 'data_nascimento', 
                      'cidade', 'estado', 'tags_favoritas')
        }),
    )
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = BaseUserAdmin.list_filter + ('tags_favoritas',)
    filter_horizontal = ('tags_favoritas',)