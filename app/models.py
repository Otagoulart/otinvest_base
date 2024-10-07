from django.db import models
from django.contrib.auth.models import User



# Modelo para Dúvidas
class Duvida(models.Model):
    titulo = models.CharField(max_length=255, default="Sem título")  # Defina um valor padrão
    autor = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)  # Tornar nulável
    duvida = models.TextField()

    class Meta:
        verbose_name_plural = "Duvidas"

    def __str__(self):
        return self.titulo  # Exibir o título como representação
        
class Comentario(models.Model):
    duvida = models.ForeignKey(Duvida, related_name="comentarios", on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentário de {self.autor} em {self.duvida}"

        
class Investidor(models.Model):
    id_investidor = models.AutoField(primary_key=True)  # Este é o campo principal
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)  # Associa um Investidor a um User
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11)
    datanasc = models.DateField(null=True, blank=True)
    endereco = models.CharField(max_length=255)
    cidade = models.CharField(max_length=100)
    senha = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Investidores"

    def __str__(self):
        return f"{self.nome} - {self.id_investidor}"


# Modelo para Segurança
class Seguranca(models.Model):
    titulo = models.CharField(max_length=50)
    dicas = models.TextField()
    investidor = models.ForeignKey(Investidor, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Seguranças"

    def __str__(self):
        return self.titulo

# Modelo para Contato
class Contato(models.Model):
    numero = models.CharField(max_length=15)
    email = models.EmailField()
    relato_feedback = models.TextField()
    investidor = models.ForeignKey(Investidor, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Contatos"

    def __str__(self):
        return self.email

# Modelo para Tipos de Investimentos
class TipoInvest(models.Model):
    tipo_de_investimento = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    relato = models.TextField()
    dicas = models.TextField()
    investidor = models.ForeignKey(Investidor, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Tipos de Investimentos"

    def __str__(self):
        return self.tipo_de_investimento

# Modelo para Corretoras
class Corretora(models.Model):
    nome = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    avaliacao = models.FloatField()
    investidor = models.ForeignKey(Investidor, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Corretoras"

    def __str__(self):
        return self.nome

class PerfilInvest(models.Model):
    idperfilinvest = models.BigAutoField(primary_key=True)  # Exemplo correto
    investidor = models.ForeignKey(Investidor, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=50)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    id_capitalinvest = models.DecimalField(max_digits=10, decimal_places=2, default=100)

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
