
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Investidor
from .models import Duvida
from .models import Comentario
from .models import Answer
from .models import Corretora, TipoInvestimento, PerfilInvest, SimuladorInvestimento, Arquivo

class RegisterForm(UserCreationForm):
    # Campos relacionados ao investidor
    nome = forms.CharField(max_length=100, required=True)
    cpf = forms.CharField(max_length=11, required=True)
    datanasc = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    endereco = forms.CharField(max_length=255, required=True)
    cidade = forms.CharField(max_length=100, required=True)
    
    # O campo 'email' já está no UserCreationForm, mas é opcional, então definimos como obrigatório aqui
    email = forms.EmailField(required=True)

    class Meta:
        model = User  # Modelo para a parte de autenticação
        fields = ['username', 'email', 'password1', 'password2', 'nome', 'cpf', 'datanasc', 'endereco', 'cidade']
        widgets = {
            'senha': forms.PasswordInput(),  # Campo de senha oculto
        }

    def save(self, commit=True):
        user = super().save(commit)
        usuario = Investidor(
            user=user,
            nome=self.cleaned_data['nome'],
            datanasc=self.cleaned_data['datanasc'],
            cpf=self.cleaned_data['cpf'],
            endereco=self.cleaned_data['endereco'],
            cidade=self.cleaned_data['cidade'],
        )
        if commit:
            usuario.save()
        return user

class DuvidaForm(forms.ModelForm):
    class Meta:
        model = Duvida
        fields = ['titulo', 'duvida']  # Certifique-se de que 'titulo' está aqui


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']

class QuizForm(forms.Form):
    answer_1 = forms.ChoiceField(label="Qual é o seu principal objetivo de investimento?", choices=[])
    answer_2 = forms.ChoiceField(label="Qual é o seu nível de experiência com investimentos?", choices=[])
    answer_3 = forms.ChoiceField(label="Qual é a sua tolerância ao risco?", choices=[])
    answer_4 = forms.ChoiceField(label="Por quanto tempo você pretende manter seus investimentos?", choices=[])

class InvestimentoForm(forms.ModelForm):
    class Meta:
        model = PerfilInvest
        fields = ['descricao', 'capital_investido', 'corretora', 'tipo_investimento']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pega o user dos kwargs ou None se não for passado
        super(InvestimentoForm, self).__init__(*args, **kwargs)

        # Se o usuário foi passado, ajuste os campos conforme necessário
        if user is not None:
            self.fields['corretora'].queryset = Corretora.objects.filter()  # Aqui você pode filtrar baseado no user


class SimuladorInvestimentoForm(forms.ModelForm):
    class Meta:
        model = SimuladorInvestimento
        fields = ['valor_investido', 'periodo', 'perfil_risco']
        widgets = {
            'perfil_risco': forms.RadioSelect(choices=[
                ('Seguro, Sugestão: Tesouro direto ', 'Busco primeiro segurança, não quero perder dinheiro'),
                ('Moderado, Sugestão: Renda Fixa, Fundos Imobiliários (FIIs)', 'Tolero pequenas oscilações, mas nada que arrisque meu patrimônio'),
                ('Arrojado, Sugestão: Ações', 'Aceito algumas perdas, em busca de ganhos maiores no longo prazo'),
                ('Alto risco, Sugestão: Criptomoedas:', 'Busco a maior rentabilidade no curto prazo, assumindo altos riscos')
            ])
        }


class ArquivoForm(forms.ModelForm):
    class Meta:
        model = Arquivo
        fields = ['titulo', 'arquivo', 'descricao']