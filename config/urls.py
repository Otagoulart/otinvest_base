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
    exclui_comentario
)
from app.views import quiz_view
urlpatterns = [

    path('admin/', admin.site.urls),
    path('', include("app.urls")),
   
    # URLs de autenticação
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),


    path('perfil-invest/', PerfilInvestView.as_view(), name='perfilinvest'),
    path('contato/', ContatoView.as_view(), name='contato'),
    path('seguranca/', SegurancaView.as_view(), name='seguranca'),
    path('corretoras/', CorretoraView.as_view(), name='corretoras'),
    path('tipo-investimento/', TipoInvestView.as_view(), name='tipoinvest'),

    #forum
    path('forum/', views.lista_duvidas, name='forum_home'),
    path('duvidas/', views.lista_duvidas, name='lista_duvidas'),
    path('duvidas/nova/', views.cria_duvida, name='cria_duvida'),
    path('duvidas/<int:id>/', views.detalhes_duvida, name='detalhes_duvida'),
    path('duvidas/edita/<int:id>/', edita_duvida, name='edita_duvida'),
    path('duvidas/exclui/<int:id>/', exclui_duvida, name='exclui_duvida'),
    path('comentario/<int:comentario_id>/edita/', edita_comentario, name='edita_comentario'),
    path('comentario/<int:comentario_id>/exclui/', exclui_comentario, name='exclui_comentario'),

    path('quiz/', quiz_view, name='quiz'),

    
]


