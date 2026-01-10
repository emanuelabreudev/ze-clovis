from django.db import models

class Config(models.Model):
    """
    Modelo para configurações globais do sistema
    
    Obs.: Utilize get_instance() para pegar as configurações globais
    do app (padrão Singleton)
    """

    preco = models.FloatField(null=False, blank=False)
    desconto = models.PositiveIntegerField(null=False, blank=False, default=30)
    vagas = models.PositiveIntegerField(null=False, blank=False)

    @classmethod
    def get_instance(cls):
        """Retorna a instância única de configuração (padrão Singleton)"""
        if not cls.objects.first():
            cls(preco=10.00, vagas=50, desconto=30).save()
        return cls.objects.first()
    
    def __str__(self):
        return 'Configurações do Sistema'