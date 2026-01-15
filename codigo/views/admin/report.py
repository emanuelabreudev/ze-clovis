from django.views.generic.base import TemplateView
from django.http import HttpResponse
from datetime import datetime, timedelta
from codigo.models import Ficha
import csv


class AdminReport(TemplateView):
    """
    Tela de relatório do sistema
    """
    template_name = 'login/report.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
       
        hoje = datetime.now().date()
        
        
        fichas_hoje = Ficha.objects.filter(
            horario_entrada__date=hoje
        )
        
        
        total_veiculos = fichas_hoje.count()
        entradas = fichas_hoje.count()
        saidas = fichas_hoje.filter(pago=True).count()
        valor_total = sum([f.valor for f in fichas_hoje.filter(pago=True) if f.valor])
        
        context['data'] = hoje.strftime('%d/%m/%Y')
        context['total_veiculos'] = total_veiculos
        context['entradas'] = entradas
        context['saidas'] = saidas
        context['valor_total'] = f'{valor_total:.2f}' if valor_total else '0.00'
        
        return context
    
    def post(self, *args, **kwargs):
        """
        Gera CSV do relatório para download
        """
        hoje = datetime.now().date()
        fichas_hoje = Ficha.objects.filter(horario_entrada__date=hoje)
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="relatorio_{hoje.strftime("%Y%m%d")}.csv"'
        response.write('\ufeff')  
        
        writer = csv.writer(response)
        writer.writerow(['FICHA', 'Status', 'Horário de Entrada', 'Horário de Saída', 'Nome', 'Preço'])
        
        for ficha in fichas_hoje:
            writer.writerow([
                ficha.id,
                'Pago' if ficha.pago else 'Estacionado',
                ficha.horario_entrada.strftime('%d/%m/%Y às %H:%M') if ficha.horario_entrada else '--',
                ficha.horario_saida.strftime('%d/%m/%Y às %H:%M') if ficha.horario_saida else '--',
                ficha.usuario.nome if ficha.usuario else 'Comum',
                f'R$ {ficha.valor:.2f}' if ficha.valor else '--'
            ])
        
        return response