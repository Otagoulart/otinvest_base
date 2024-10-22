from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Duvida, Investidor, Corretora, Seguranca, Question, Answer, Contato, Comentario, Arquivo,SimuladorInvestimento
from .forms import RegisterForm, ComentarioForm, DuvidaForm, QuizForm,InvestimentoForm,ArquivoForm,SimuladorInvestimentoForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import PerfilInvest
from django.shortcuts import render, get_object_or_404, redirect,render, redirect,get_object_or_404
from decimal import Decimal


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')

class ContatoView(View):
    def get(self, request):
        contatos = Contato.objects.all()
        return render(request, 'contato.html', {'contatos': contatos})

class SegurancaView(View):
    def get(self, request):
        seguranca = Seguranca.objects.all()
        return render(request, 'forum.html', {'seguranca': seguranca})

class CorretoraView(View):
    def get(self, request):
        corretoras = Corretora.objects.all()
        return render(request, 'ondeinvestir.html', {'corretoras': corretoras})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            if not Investidor.objects.filter(user=user).exists():
                Investidor.objects.create(user=user)
            else:
                messages.warning(request, "Usuário já registrado como investidor.")
                return redirect('login')
            login(request, user)
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect('index')
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

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
                messages.error(request, "Usuário ou senha inválidos.")
        else:
            messages.error(request, "Dados inválidos.")
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Você saiu com sucesso.")
    return redirect('index')

@login_required
def lista_duvidas(request):
    duvidas = Duvida.objects.all()
    return render(request, 'forum/lista_duvidas.html', {'duvidas': duvidas})

@login_required
def detalhes_duvida(request, id):
    duvida = get_object_or_404(Duvida, id=id)
    comentarios = duvida.comentarios.all()
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentarios = duvida.comentarios.order_by('-data_criacao')
            comentario = form.save(commit=False)
            comentario.autor = request.user
            comentario.duvida = duvida
            comentario.save()
            return redirect('detalhes_duvida', id=duvida.id)
    else:
        form = ComentarioForm()
    return render(request, 'forum/detalhes_duvida.html', {'duvida': duvida, 'comentarios': comentarios, 'form': form})

@login_required
def cria_duvida(request):
    if request.method == 'POST':
        form = DuvidaForm(request.POST)
        if form.is_valid():
            titulo = form.cleaned_data['titulo']
            if Duvida.objects.filter(titulo=titulo).exists():
                messages.error(request, "Já existe uma dúvida com esse título.")
                return render(request, 'forum/cria_duvida.html', {'form': form})
            duvida = form.save(commit=False)
            duvida.autor = request.user
            duvida.save()
            messages.success(request, "Dúvida criada com sucesso!")
            return redirect('lista_duvidas')
    else:
        form = DuvidaForm()
    return render(request, 'forum/cria_duvida.html', {'form': form})

@login_required
def edita_duvida(request, id):
    duvida = get_object_or_404(Duvida, id=id)
    if request.user != duvida.autor and not request.user.is_staff:
        messages.error(request, "Você não tem permissão para editar esta dúvida.")
        return redirect('detalhes_duvida', id=duvida.id)
    if request.method == 'POST':
        form = DuvidaForm(request.POST, instance=duvida)
        if form.is_valid():
            titulo = form.cleaned_data['titulo']
            if Duvida.objects.exclude(id=duvida.id).filter(titulo=titulo).exists():
                messages.error(request, "Já existe uma dúvida com esse título.")
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
            return redirect('detalhes_duvida', id=comentario.duvida.id)
    else:
        form = ComentarioForm(instance=comentario)
    return render(request, 'forum/edita_comentario.html', {'form': form, 'duvida': comentario.duvida})

@login_required
def exclui_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    if request.user != comentario.autor and not request.user.is_superuser:
        messages.error(request, "Você não tem permissão para excluir este comentário.")
        return redirect('detalhes_duvida', id=comentario.duvida.id)
    if request.method == 'POST':
        comentario.delete()
        messages.success(request, "Comentário excluído com sucesso!")
        return redirect('detalhes_duvida', id=comentario.duvida.id)
    return render(request, 'forum/exclui_comentario.html', {'comentario': comentario})

    class QuizForm(forms.Form):
        pass

def quiz_view(request):
    questions = Question.objects.all()
    if request.method == 'POST':
        answer_ids = [request.POST.get(f'answer_{question.id}') for question in questions]
        results = {
            "Investidor Agressivo": 0,
            "Investidor Moderado": 0,
            "Investidor Conservador": 0,
            "Investidor Especulativo": 0,
        }
        for answer_id in answer_ids:
            if answer_id:
                try:
                    category = Answer.objects.get(id=answer_id).category
                    results[category] += 1
                except Answer.DoesNotExist:
                    continue
        max_category = max(results, key=results.get)
        return render(request, 'quiz/quiz_result.html', {'result': max_category})
    else:
        quiz_form = QuizForm()
        for question in questions:
            quiz_form.fields[f'answer_{question.id}'] = forms.ChoiceField(
                choices=[(answer.id, answer.text) for answer in Answer.objects.filter(question=question)],
                widget=forms.RadioSelect,
                label=question.text
            )
        return render(request, 'quiz/quiz.html', {'form': quiz_form, 'questions': questions})

@login_required
def perfil_usuario(request):
    investidor = get_object_or_404(Investidor, user=request.user)
    return render(request, 'perfil/perfil.html', {'investidor': investidor})


@login_required
def editar_perfil(request):
    user = request.user  
    investidor = Investidor.objects.get(user=request.user)
    if request.method == 'POST':
        investidor.nome = request.POST['nome']
        investidor.cpf = request.POST['cpf']
        investidor.datanasc = request.POST['datanasc']
        user.email = request.POST['email']
        investidor.endereco = request.POST['endereco']
        investidor.cidade = request.POST['cidade']
        investidor.save()
        user.save()
        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('perfil_usuario')
    return render(request, 'perfil/editar_perfil.html', {'investidor': investidor})


@login_required
def trocar_senha(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            messages.success(request, 'Senha atualizada com sucesso!')
            return redirect('perfil_usuario')
        else:
            messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'perfil/trocar_senha.html', {'form': form})


@login_required
def deletar_conta(request):

    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Conta deletada com sucesso.')
        return redirect('/') 
    return render(request, 'perfil/deletar_conta.html')

@login_required
def investimentos(request):
    investimentos = PerfilInvest.objects.filter(investidor__user=request.user)

    return render(request, 'investi/investimentos.html', {'investimentos': investimentos})


@login_required
def meus_investimentos(request):
    try:
        investidor = request.user.investidor
    except Investidor.DoesNotExist:
        investidor = Investidor.objects.create(user=request.user)

    if request.method == 'POST':
        form = InvestimentoForm(request.POST, user=request.user)
        if form.is_valid():
            perfil_invest = form.save(commit=False)
            perfil_invest.investidor = investidor  
            perfil_invest.save() 
            return redirect('investimentos') 
    else:
        form = InvestimentoForm(user=request.user)

    return render(request, 'investi/meus_investimentos.html', {'form': form})


@login_required
def editar_investimento(request, pk):
    investimento = get_object_or_404(PerfilInvest, pk=pk, investidor__user=request.user)
    
    if request.method == 'POST':
        form = InvestimentoForm(request.POST, instance=investimento, user=request.user) 
        if form.is_valid():
            perfil_invest = form.save(commit=False) 
            perfil_invest.investidor = request.user.investidor 
            perfil_invest.save()  
            return redirect('investimentos')
    else:
        form = InvestimentoForm(instance=investimento, user=request.user)  
    
    return render(request, 'investi/editar_investimento.html', {'form': form})

@login_required
def excluir_investimento(request, pk):
    investimento = get_object_or_404(PerfilInvest, pk=pk, investidor__user=request.user)
    if request.method == 'POST':
        investimento.delete()
        return redirect('investimentos')
    return render(request, 'investi/confirmar_exclusao.html', {'investimento': investimento})

def sobre(request):
    return render(request, 'sobre.html')


def simulador_investimento(request):
    if request.method == 'POST':
        form = SimuladorInvestimentoForm(request.POST)
        if form.is_valid():
            simulacao = form.save(commit=False)
            if simulacao.perfil_risco == 'Seguro, Sugestão: Tesouro direto':
                retorno = simulacao.valor_investido * (Decimal(1) + Decimal(0.10) * simulacao.periodo / Decimal(12))  
            elif simulacao.perfil_risco == 'Moderado, Sugestão: Renda Fixa, Fundos Imobiliários (FIIs)':
                retorno = simulacao.valor_investido * (Decimal(1) + Decimal(0.08) * simulacao.periodo / Decimal(12)) 
            elif simulacao.perfil_risco == 'Arrojado, Sugestão: Ações':
                retorno = simulacao.valor_investido * (Decimal(1) + Decimal(0.12) * simulacao.periodo / Decimal(12)) 
            else:
                retorno = simulacao.valor_investido * (Decimal(1) + Decimal(0.30) * simulacao.periodo / Decimal(12)) 

            simulacao.resultado = retorno
            simulacao.usuario = request.user
            simulacao.save()
            return redirect('resultado_simulacao', simulacao_id=simulacao.id)
    else:
        form = SimuladorInvestimentoForm()

    simulacoes_anteriores = SimuladorInvestimento.objects.filter(usuario=request.user)


    return render(request, 'simulacao/simulador_investimento.html', {'form': form, 'simulacoes_anteriores': simulacoes_anteriores})


def resultado_simulacao(request, simulacao_id):
    simulacao = SimuladorInvestimento.objects.get(id=simulacao_id)
    return render(request,'simulacao/resultado_simulacao.html', {'simulacao': simulacao})

@login_required
def excluir_simulacao(request, simulacao_id):
    simulacao = get_object_or_404(SimuladorInvestimento, id=simulacao_id, usuario=request.user)
    if request.method == 'POST':
        simulacao.delete()
        messages.success(request, "Simulação excluída com sucesso.")
        return redirect('simulador_investimento')
    return render(request, 'simulacao/excluir_simulacao.html', {'simulacao': simulacao})


@login_required
def lista_arquivos(request):
    arquivos = Arquivo.objects.filter(usuario=request.user)
    return render(request, 'arquivo/lista_arquivos.html', {'arquivos': arquivos})

@login_required
def upload_arquivo(request):
    if request.method == 'POST':
        form = ArquivoForm(request.POST, request.FILES)
        if form.is_valid():
            arquivo = form.save(commit=False)
            arquivo.usuario = request.user
            arquivo.save()
            return redirect('lista_arquivos')
    else:
        form = ArquivoForm()
    return render(request, 'arquivo/upload_arquivo.html', {'form': form})

@login_required
def edita_arquivo(request, id):
    arquivo = get_object_or_404(Arquivo, id=id, usuario=request.user)
    if request.method == 'POST':
        form = ArquivoForm(request.POST, request.FILES, instance=arquivo)
        if form.is_valid():
            form.save()
            return redirect('lista_arquivos')
    else:
        form = ArquivoForm(instance=arquivo)
    return render(request, 'arquivo/edita_arquivo.html', {'form': form})

@login_required
def exclui_arquivo(request, id):
    arquivo = get_object_or_404(Arquivo, id=id, usuario=request.user)
    if request.method == 'POST':
        arquivo.delete()
        return redirect('lista_arquivos')
    return render(request, 'arquivo/exclui_arquivo.html', {'arquivo': arquivo})
