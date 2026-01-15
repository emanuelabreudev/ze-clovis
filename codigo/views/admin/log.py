from django.views.generic.base import TemplateView
from codigo.models import Ficha
from datetime import datetime


class AdminLog(TemplateView):
    """
    Tela de log de fichas com filtros
    """

    template_name = 'login/token-log.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
     
        fichas = Ficha.objects.all().order_by('-id')
        
 
        nome = self.request.GET.get('nome', '').strip()
        if nome:
            fichas = fichas.filter(usuario__nome__icontains=nome)
            context['nome_filter'] = nome
        
      
        data = self.request.GET.get('data', '').strip()
        if data:
            try:
                data_obj = datetime.strptime(data, '%Y-%m-%d').date()
                fichas = fichas.filter(horario_entrada__date=data_obj)
                context['data_filter'] = data
            except ValueError:
                pass
        
      
        status = self.request.GET.get('status', '').strip()
        if status:
            if status == 'pago':
                fichas = fichas.filter(pago=True)
            elif status == 'estacionado':
                fichas = fichas.filter(pago=False)
            context['status_filter'] = status
        
        valor_min = self.request.GET.get('valor_min', '').strip()
        valor_max = self.request.GET.get('valor_max', '').strip()
        
        if valor_min:
            try:
                fichas = fichas.filter(valor__gte=float(valor_min))
                context['valor_min_filter'] = valor_min
            except ValueError:
                pass
        
        if valor_max:
            try:
                fichas = fichas.filter(valor__lte=float(valor_max))
                context['valor_max_filter'] = valor_max
            except ValueError:
                pass
        
        context['estacionados'] = fichas
        return context