from django.contrib import admin
from .models import Comentario, Duvida, Investidor, PerfilInvest, Seguranca, Contato, Corretora
from .models import Question, Answer
from .models import Corretora, TipoInvestimento,Arquivo
class ContatoInline(admin.TabularInline):

    model = Contato
    extra = 1  # Permite adicionar uma nova entrada sem sair da página



class CorretoraInline(admin.TabularInline):
    model = Corretora
    extra = 1  # Permite adicionar uma nova entrada sem sair da página

class InvestidorAdmin(admin.ModelAdmin):
    list_display = ["id_investidor", "nome", "cpf", "datanasc", "endereco", "cidade", "email"]
    search_fields = ["nome", "cpf", "email"]
    inlines = [ContatoInline, CorretoraInline]
    list_filter = ["cidade"]  # Adicionando filtro por cidade, se necessário
    ordering = ["nome"]  # Ordenação por nome


class DuvidaAdmin(admin.ModelAdmin):
    list_display = ["id", "duvida"]
    search_fields = ["duvida"]
    ordering = ["duvida"]  # Ordenação por duvida

class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['id', 'duvida', 'autor', 'data_criacao', 'texto']
    search_fields = ['duvida__duvida', 'autor__username', 'texto']
    list_filter = ['data_criacao', 'autor']
    ordering = ['-data_criacao']  # Exibe os comentários mais recentes primeiro


class PerfilInvestAdmin(admin.ModelAdmin):
    list_display = ["id_capitalinvest", "descricao", "salario", "investidor"]
    search_fields = ["descricao", "investidor__nome"]
    ordering = ["id_capitalinvest"]  # Ordenação por id_capitalinvest


class SegurancaAdmin(admin.ModelAdmin):
    list_display = ["id", "titulo", "investidor"]
    search_fields = ["titulo", "investidor__nome"]
    ordering = ["titulo"]  # Ordenação por título


class ContatoAdmin(admin.ModelAdmin):
    list_display = ["id", "numero", "email", "investidor"]
    search_fields = ["email", "numero", "investidor__nome"]
    ordering = ["investidor"]  # Ordenação por investidor



class QuestionAdmin(admin.ModelAdmin):
    list_display = ["id", "text"]
    search_fields = ["text"]
    ordering = ["text"]

class AnswerAdmin(admin.ModelAdmin):
    list_display = ["id", "question", "text", "category"]
    search_fields = ["text", "question__text"]
    list_filter = ["category"]
    ordering = ["question", "text"]

from django.contrib import admin


# Registro das models no admin
@admin.register(Corretora)
class CorretoraAdmin(admin.ModelAdmin):
    list_display = ('nome', 'avaliacao', 'pais')  # Colunas visíveis no admin
    search_fields = ('nome', 'pais')  # Adicionar campo de busca
    list_filter = ('pais', 'avaliacao')  # Filtros laterais

@admin.register(TipoInvestimento)
class TipoInvestimentoAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'risco', 'retorno_esperado')  # Colunas visíveis no admin
    search_fields = ('tipo',)  # Campo de busca por tipo de investimento
    list_filter = ('risco',)  # Filtros laterais para risco


@admin.register(Arquivo)
class ArquivoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'data_envio']
    search_fields = ['nome', 'usuario__username']
    list_filter = ['data_envio', 'usuario']
    ordering = ['-data_envio']

admin.site.register(Duvida)
admin.site.register(Investidor)
admin.site.register(PerfilInvest)
admin.site.register(Seguranca)
admin.site.register(Contato)
admin.site.register(Comentario)
admin.site.register(Question)
admin.site.register(Answer)
