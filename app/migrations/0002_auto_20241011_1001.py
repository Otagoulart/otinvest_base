from django.db import migrations

def create_questions_and_answers(apps, schema_editor):
    Question = apps.get_model('app', 'Question')  # Substitua 'app' pelo nome do seu aplicativo
    Answer = apps.get_model('app', 'Answer')

    # Criar perguntas
    q1 = Question.objects.create(text="Qual é o seu principal objetivo de investimento?")
    q2 = Question.objects.create(text="Qual é o seu nível de experiência com investimentos?")
    q3 = Question.objects.create(text="Qual é a sua tolerância ao risco?")
    q4 = Question.objects.create(text="Por quanto tempo você pretende manter seus investimentos?")

    # Criar respostas para a pergunta 1
    Answer.objects.create(question=q1, text="Aumentar meu patrimônio a longo prazo.", category="Investidor Agressivo")
    Answer.objects.create(question=q1, text="Gerar uma renda adicional.", category="Investidor Moderado")
    Answer.objects.create(question=q1, text="Preservar meu capital.", category="Investidor Conservador")
    Answer.objects.create(question=q1, text="Aproveitar oportunidades de curto prazo.", category="Investidor Especulativo")

    # Criar respostas para a pergunta 2
    Answer.objects.create(question=q2, text="Sou um investidor experiente.", category="Investidor Agressivo")
    Answer.objects.create(question=q2, text="Tenho algum conhecimento, mas sou iniciante.", category="Investidor Moderado")
    Answer.objects.create(question=q2, text="Conheço o básico, mas não investi muito.", category="Investidor Conservador")
    Answer.objects.create(question=q2, text="Não tenho experiência em investimentos.", category="Investidor Especulativo")

    # Criar respostas para a pergunta 3
    Answer.objects.create(question=q3, text="Estou disposto a assumir riscos altos para retornos maiores.", category="Investidor Agressivo")
    Answer.objects.create(question=q3, text="Prefiro um equilíbrio entre risco e retorno.", category="Investidor Moderado")
    Answer.objects.create(question=q3, text="Sou cauteloso e prefiro investimentos de baixo risco.", category="Investidor Conservador")
    Answer.objects.create(question=q3, text="Não quero correr riscos; prefiro segurança total.", category="Investidor Especulativo")

    # Criar respostas para a pergunta 4
    Answer.objects.create(question=q4, text="Mais de 10 anos.", category="Investidor Agressivo")
    Answer.objects.create(question=q4, text="De 5 a 10 anos.", category="Investidor Moderado")
    Answer.objects.create(question=q4, text="De 1 a 5 anos.", category="Investidor Conservador")
    Answer.objects.create(question=q4, text="Menos de 1 ano.", category="Investidor Especulativo")

def add_initial_data(apps, schema_editor):
    Corretora = apps.get_model('app', 'Corretora')
    TipoInvestimento = apps.get_model('app', 'TipoInvestimento')

    # Dados para Corretoras
    corretoras = [
        Corretora(nome='XP Investimentos', avaliacao=4.7, pais='Brasil'),
        Corretora(nome='Rico Investimentos', avaliacao=4.3, pais='Brasil'),
        Corretora(nome='Clear Corretora', avaliacao=4.5, pais='Brasil'),
        Corretora(nome='Avenue Securities', avaliacao=4.2, pais='EUA'),
        Corretora(nome='Inter Invest', avaliacao=4.0, pais='Brasil'),
    ]

    # Salvar dados de corretoras
    for corretora in corretoras:
        corretora.save()

    # Dados para Tipos de Investimentos
    tipos_investimento = [
        TipoInvestimento(tipo='Ações', descricao='Investimento em ações de empresas listadas na bolsa de valores.', risco='Alto', retorno_esperado=12.5),
        TipoInvestimento(tipo='Renda Fixa', descricao='Títulos emitidos por governos e empresas com juros fixos.', risco='Baixo', retorno_esperado=5.0),
        TipoInvestimento(tipo='Fundos Imobiliários', descricao='Investimento em fundos que possuem imóveis ou direitos imobiliários.', risco='Moderado', retorno_esperado=8.0),
        TipoInvestimento(tipo='Criptomoedas', descricao='Investimento em moedas digitais, como Bitcoin e Ethereum.', risco='Alto', retorno_esperado=20.0),
        TipoInvestimento(tipo='Tesouro Direto', descricao='Títulos públicos emitidos pelo governo brasileiro.', risco='Baixo', retorno_esperado=4.5),
    ]

    # Salvar dados de tipos de investimento
    for tipo in tipos_investimento:
        tipo.save()
class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),  # Ajuste para a última migração do seu aplicativo
    ]

    operations = [
        migrations.RunPython(create_questions_and_answers),
        migrations.RunPython(add_initial_data),
    ]
