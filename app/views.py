
from django.shortcuts import render, redirect, get_object_or_404
from .models import *  # Certifique-se de que você só importa o que precisa
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Duvida, Investidor, PerfilInvest, Corretora, TipoInvest, Seguranca  # Adicione os modelos que você utiliza
# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, ComentarioForm
from django.contrib.auth import login, update_session_auth_hash
from .forms import DuvidaForm
from django.contrib.auth.decorators import login_required
from .models import Question, Answer
from .forms import QuizForm
from .forms import QuizForm  # Certifique-se de que este formulário está correto
from django import forms
from django.shortcuts import render
from .models import Question, Answer

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')



# # View para cadastro de investidores
# class InvestidorView(View):
#     def get(self, request):
#         form = InvestidorForm()  # Cria uma instância vazia do formulário
#         return render(request, 'cadastro.html', {'form': form})

#     def post(self, request):
#         form = InvestidorForm(request.POST)
#         if form.is_valid():
#             form.save()  # Salva o formulário se for válido
#             return redirect('sucesso')  # Redireciona para a URL de sucesso
#         return render(request, 'cadastro.html', {'form': form})  # Retorna o formulário com erros se inválido

class PerfilInvestView(View):
    def get(self, request):
        perfis_invest = PerfilInvest.objects.all()
        return render(request, 'perfilinvest.html', {'perfilinvest': perfis_invest})

# View para contato
class ContatoView(View):
    def get(self, request):
        contatos = Contato.objects.all()
        return render(request, 'contato.html', {'contatos': contatos})

# View para segurança
class SegurancaView(View):
    def get(self, request):
        seguranca = Seguranca.objects.all()
        return render(request, 'forum.html', {'seguranca': seguranca})

# View para corretoras
class CorretoraView(View):
    def get(self, request):
        corretoras = Corretora.objects.all()
        return render(request, 'ondeinvestir.html', {'corretoras': corretoras})

# View para tipos de investimento
class TipoInvestView(View):
    def get(self, request):
        tipos_invest = TipoInvest.objects.all()
        return render(request, 'investimento.html', {'tipoinvest': tipos_invest})



def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Salva o User
            
            # Verifica se já existe um Investidor associado ao User
            if not Investidor.objects.filter(user=user).exists():
                Investidor.objects.create(user=user)  # Cria um Investidor associado ao User
            else:
                messages.warning(request, "Usuário já registrado como investidor.")
                return redirect('login')  # Ou redirecione para outra página
            
            login(request, user)  # Faz login automaticamente após o registro
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect('index')  # Redireciona para a página inicial ou de perfil após o registro
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = RegisterForm()  # Formulário vazio para GET

    return render(request, 'registration/register.html', {'form': form})  # Aponte para o template correto


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid form data.")
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('index')

#forum
@login_required
def lista_duvidas(request):
    duvidas = Duvida.objects.all()
    return render(request, 'forum/lista_duvidas.html', {'duvidas': duvidas})

# Detalha uma dúvida específica
@login_required
def detalhes_duvida(request, id):
    duvida = get_object_or_404(Duvida, id=id)
    comentarios = duvida.comentarios.all()

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.autor = request.user
            comentario.duvida = duvida
            comentario.save()
            return redirect('detalhes_duvida', id=duvida.id)
    else:
        form = ComentarioForm()

    return render(request, 'forum/detalhes_duvida.html', {
        'duvida': duvida,
        'comentarios': comentarios,
        'form': form
    })

# Cria uma nova dúvida (autenticado)
@login_required
def cria_duvida(request):
    if request.method == 'POST':
        form = DuvidaForm(request.POST)
        if form.is_valid():
            # Verifica se já existe uma dúvida com o mesmo título
            titulo = form.cleaned_data['titulo']  # Obtém o título do formulário
            if Duvida.objects.filter(titulo=titulo).exists():  # Verifica se o título já existe
                messages.error(request, "Já existe uma dúvida com esse título. Por favor, escolha outro título.")
                return render(request, 'forum/cria_duvida.html', {'form': form})  # Retorna o formulário com mensagem de erro
            
            # Cria uma nova instância de Duvida
            duvida = form.save(commit=False)  # Não salva ainda
            duvida.autor = request.user  # Define o autor como o usuário autenticado
            duvida.save()  # Agora salva a dúvida
            
            messages.success(request, "Dúvida criada com sucesso!")  # Mensagem de sucesso
            return redirect('lista_duvidas')  # Redireciona para a lista de dúvidas
    else:
        form = DuvidaForm()
    
    return render(request, 'forum/cria_duvida.html', {'form': form})
@login_required
def edita_duvida(request, id):
    duvida = get_object_or_404(Duvida, id=id)

    # Verifica se o usuário é o autor ou um administrador
    if request.user != duvida.autor and not request.user.is_staff:
        messages.error(request, "Você não tem permissão para editar esta dúvida.")
        return redirect('detalhes_duvida', id=duvida.id)

    if request.method == 'POST':
        form = DuvidaForm(request.POST, instance=duvida)
        if form.is_valid():
            titulo = form.cleaned_data['titulo']
            if Duvida.objects.exclude(id=duvida.id).filter(titulo=titulo).exists():
                messages.error(request, "Já existe uma dúvida com esse título. Por favor, escolha outro título.")
                return render(request, 'forum/edita_duvida.html', {'form': form, 'duvida': duvida})
            form.save()
            messages.success(request, "Dúvida atualizada com sucesso!")
            return redirect('detalhes_duvida', id=duvida.id)
    else:
        form = DuvidaForm(instance=duvida)

    return render(request, 'forum/edita_duvida.html', {'form': form, 'duvida': duvida})



@login_required
def exclui_duvida(request, id):
    duvida = get_object_or_404(Duvida, id=id)

    # Verifica se o usuário é o autor ou um administrador
    if request.user != duvida.autor and not request.user.is_staff:
        messages.error(request, "Você não tem permissão para excluir esta dúvida.")
        return redirect('detalhes_duvida', id=duvida.id)

    if request.method == 'POST':
        duvida.delete()
        messages.success(request, "Dúvida excluída com sucesso!")
        return redirect('lista_duvidas')

    return render(request, 'forum/exclui_duvida.html', {'duvida': duvida})


@login_required
def edita_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)

    if request.method == 'POST':
        form = ComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            messages.success(request, "Comentário atualizado com sucesso!")
            return redirect('detalhes_duvida', id=comentario.duvida.id)  # Aqui passamos o ID da dúvida
    else:
        form = ComentarioForm(instance=comentario)

    return render(request, 'forum/edita_comentario.html', {'form': form, 'duvida': comentario.duvida})


@login_required
def exclui_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    
    # Verifica se o usuário é o autor ou um admin
    if request.user != comentario.autor and not request.user.is_superuser:
        messages.error(request, "Você não tem permissão para excluir este comentário.")
        return redirect('detalhes_duvida', id=comentario.duvida.id)

    if request.method == 'POST':
        comentario.delete()
        messages.success(request, "Comentário excluído com sucesso!")
        return redirect('detalhes_duvida', id=comentario.duvida.id)

    return render(request, 'forum/exclui_comentario.html', {'comentario': comentario})

class QuizForm(forms.Form):
    pass  # Formulário vazio; os campos serão gerados dinamicamente na view

def quiz_view(request):
    questions = Question.objects.all()
    
    if request.method == 'POST':
        # Captura as respostas
        answer_ids = [request.POST.get(f'answer_{question.id}') for question in questions]

        # Contar as categorias de cada resposta
        results = {
            "Investidor Agressivo": 0,
            "Investidor Moderado": 0,
            "Investidor Conservador": 0,
            "Investidor Especulativo": 0,
        }

        for answer_id in answer_ids:
            if answer_id:  # Verifica se a resposta foi fornecida
                try:
                    category = Answer.objects.get(id=answer_id).category
                    results[category] += 1
                except Answer.DoesNotExist:
                    continue  # Ignora se a resposta não existe

        # Determinar o tipo de investidor
        max_category = max(results, key=results.get)

        return render(request, 'quiz_result.html', {'result': max_category})

    else:
        # Carregar as opções para cada pergunta
        quiz_form = QuizForm()
        for question in questions:
            quiz_form.fields[f'answer_{question.id}'] = forms.ChoiceField(
                choices=[(answer.id, answer.text) for answer in Answer.objects.filter(question=question)],
                widget=forms.RadioSelect,
                label=question.text
            )
        
        return render(request, 'quiz.html', {'form': quiz_form, 'questions': questions})