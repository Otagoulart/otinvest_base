from django.db import models
from django.contrib.auth.models import User


class Duvida(models.Model):
    titulo = models.CharField(max_length=255, default="Sem título")
    autor = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    duvida = models.TextField()

    class Meta:
        verbose_name_plural = "Dúvidas"

    def __str__(self):
        return self.titulo



class Comentario(models.Model):
    duvida = models.ForeignKey(Duvida, related_name="comentarios", on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentário de {self.autor} em {self.duvida}"



class Investidor(models.Model):
    id_investidor = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1, related_name='investidor')
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11)
    datanasc = models.DateField(null=True, blank=True)
    endereco = models.CharField(max_length=255)
    cidade = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Investidores"

    def __str__(self):
        return f"{self.nome} - {self.id_investidor}"



class Seguranca(models.Model):
    titulo = models.CharField(max_length=50)
    dicas = models.TextField()
    investidor = models.ForeignKey(Investidor, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Seguranças"

    def __str__(self):
        return self.titulo



class Contato(models.Model):
    numero = models.CharField(max_length=15)
    email = models.EmailField()
    relato_feedback = models.TextField()
    investidor = models.ForeignKey(Investidor, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Contatos"

    def __str__(self):
        return self.email



class Corretora(models.Model):
    nome = models.CharField(max_length=255)
    avaliacao = models.FloatField()
    pais = models.CharField(max_length=100, default="Brasil")

    class Meta:
        verbose_name_plural = "Corretoras"

    def __str__(self):
        return f"{self.nome} - {self.pais}"



class TipoInvestimento(models.Model):
    tipo = models.CharField(max_length=100)
    descricao = models.TextField()
    risco = models.CharField(max_length=50)
    retorno_esperado = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = "Tipos de Investimento"

    def __str__(self):
        return self.tipo



class PerfilInvest(models.Model):
    idperfilinvest = models.BigAutoField(primary_key=True)
    investidor = models.ForeignKey(Investidor, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=50)
    capital_investido = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    corretora = models.ForeignKey(Corretora, on_delete=models.CASCADE)
    tipo_investimento = models.ForeignKey(TipoInvestimento, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Perfis de Investimento"

    def __str__(self):
        return self.descricao



class Question(models.Model):
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text



class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.text



class SimuladorInvestimento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    valor_investido = models.DecimalField(max_digits=10, decimal_places=2)
    periodo = models.IntegerField()
    perfil_risco = models.CharField(max_length=100)
    resultado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Simulação de {self.usuario.username} - {self.valor_investido}"



class Arquivo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    arquivo = models.FileField(upload_to='arquivos/')
    descricao = models.TextField(blank=True)
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
