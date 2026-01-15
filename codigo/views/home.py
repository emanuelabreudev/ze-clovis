"""
View da tela inicial do sistema
"""
from django.views.generic.base import TemplateView


class Home(TemplateView):
    """
    Tela inicial do sistema - escolha entre Entrada ou Saída
    """
    template_name = 'home.html'