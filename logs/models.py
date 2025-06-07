from django.db import models

# Create your models here.
class LogDeAcesso(models.Model):
  STATUS_CHOICES = [
    ('sucesso', 'Sucesso'),
    ('erro', 'Erro'),
    ('atencao', 'Atenção'),
  ]

  user = models.CharField(max_length=255)
  acao = models.CharField(max_length=255)
  resultado = models.CharField(max_length=7, default='sucesso', choices=STATUS_CHOICES)
  detalhes = models.TextField(blank=True, null=True)
  data_hora = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'{self.user.email} -- {self.acao}'
