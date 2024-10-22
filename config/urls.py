"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from app import views
from app.views import *
from app.views import (
    register,
    lista_duvidas,
    cria_duvida,
    detalhes_duvida,
    edita_comentario, 
    exclui_comentario,
    perfil_usuario,
    editar_perfil,
    trocar_senha,
    deletar_conta,
    meus_investimentos
)
from app.views import quiz_view
urlpatterns = [

    path('admin/', admin.site.urls),
    path('', include("app.urls")),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('contato/', ContatoView.as_view(), name='contato'),
    path('seguranca/', SegurancaView.as_view(), name='seguranca'),
    path('corretoras/', CorretoraView.as_view(), name='corretoras'),
    path('forum/sobre', views.sobre, name='sobre'),
    path('forum/', views.lista_duvidas, name='forum_home'),
    path('duvidas/', views.lista_duvidas, name='lista_duvidas'),
    path('duvidas/nova/', views.cria_duvida, name='cria_duvida'),
    path('duvidas/<int:id>/', views.detalhes_duvida, name='detalhes_duvida'),
    path('duvidas/edita/<int:id>/', edita_duvida, name='edita_duvida'),
    path('duvidas/exclui/<int:id>/', exclui_duvida, name='exclui_duvida'),
    path('comentario/<int:comentario_id>/edita/', edita_comentario, name='edita_comentario'),
    path('comentario/<int:comentario_id>/exclui/', exclui_comentario, name='exclui_comentario'),
    path('quiz/', views.quiz_view, name='quiz'),
    path('quiz/sobre', views.sobre, name='sobre'),
    path('perfil/sobre', views.sobre, name='sobre'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('perfil/trocar_senha/', views.trocar_senha, name='trocar_senha'),
    path('perfil/deletar/', views.deletar_conta, name='deletar_conta'),
    path('investimentos/sobre', views.sobre, name='sobre'),
    path('meus_investimentos/',views.meus_investimentos, name='meus_investimentos'),
    path('investimentos/', views.investimentos, name='investimentos'),
    path('investimentos/editar/<int:pk>/', views.editar_investimento, name='editar_investimento'),
    path('investimentos/excluir/<int:pk>/', views.excluir_investimento, name='excluir_investimento'),
    path('sobre/', views.sobre, name='sobre'),
    path('simulador_investimento/sobre', views.sobre, name='sobre'),
    path('simulador_investimento/', views.simulador_investimento, name='simulador_investimento'),
    path('simulador/resultado/<int:simulacao_id>/', views.resultado_simulacao, name='resultado_simulacao'),
    path('simulacao/excluir/<int:simulacao_id>/', excluir_simulacao, name='excluir_simulacao'),
    path('perfil/lista_arquivos', views.perfil_usuario, name='perfil_usuario'),
    path('arquivos/sobre', views.sobre, name='sobre'),
    path('arquivos/', views.lista_arquivos, name='lista_arquivos'),
    path('arquivos/upload/', views.upload_arquivo, name='upload_arquivo'),
    path('arquivos/editar/<int:id>/', views.edita_arquivo, name='edita_arquivo'),
    path('arquivos/excluir/<int:id>/', views.exclui_arquivo, name='exclui_arquivo'),
]

 



    



