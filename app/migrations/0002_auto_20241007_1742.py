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

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),  # Ajuste para a última migração do seu aplicativo
    ]

    operations = [
        migrations.RunPython(create_questions_and_answers),
    ]
