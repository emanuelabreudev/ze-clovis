
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.shortcuts import redirect, reverse
from codigo.models import Admin
import secrets


class PasswordResetRequest(TemplateView):
    """
    Tela de solicitação de redefinição de senha
    """
    template_name = 'login/password_reset_request.html'
    
    def post(self, request, *args, **kwargs):
      
        email = request.POST.get('email', '').strip()
        

        
        if not email:
            messages.error(request, 'Por favor, informe o email')
            return redirect(reverse('codigo:password-reset-request'))
        
     
        if Admin.objects.filter(email=email).exists():
            admin = Admin.objects.get(email=email)
            
      
            token = secrets.token_urlsafe(32)
            
            
            request.session['reset_token'] = token
            request.session['reset_email'] = email
            
          
            reset_link = request.build_absolute_uri(
                reverse('codigo:password-reset-confirm') + f'?token={token}'
            )
            
       
            request.session['reset_link'] = reset_link
            

            
            messages.success(request, 'Link de redefinição gerado! Confira o console.')
            return redirect(reverse('codigo:password-reset-sent'))
        else:
           
            messages.info(
                request, 
                'Se este email estiver cadastrado, você receberá um link de redefinição'
            )
            return redirect(reverse('codigo:password-reset-sent'))


class PasswordResetSent(TemplateView):
    """
    Tela de confirmação de envio de email
    """
    template_name = 'login/password_reset_sent.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        context['reset_link'] = self.request.session.get('reset_link', '')
        context['reset_email'] = self.request.session.get('reset_email', '')
        return context


class PasswordResetConfirm(TemplateView):
    """
    Tela de redefinição de senha com token
    """
    template_name = 'login/password_reset_confirm.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
    
        token = self.request.GET.get('token', '')
        
    
        session_token = self.request.session.get('reset_token', '')
        session_email = self.request.session.get('reset_email', '')
        
        print(f"DEBUG GET: Token URL: '{token}'")
        print(f"DEBUG GET: Token Sessão: '{session_token}'")
        
        if token and token == session_token and session_email:
            context['token_valid'] = True
            context['admin_email'] = session_email
            context['token'] = token
        else:
            context['token_valid'] = False
            context['error_message'] = 'Link inválido ou expirado'
        
        return context
    
    def post(self, request, *args, **kwargs):
        
        token = request.GET.get('token', '')
        new_password = request.POST.get('new_password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        

        
     
        session_token = request.session.get('reset_token', '')
        session_email = request.session.get('reset_email', '')
        
        if not token or token != session_token or not session_email:
            messages.error(request, 'Link inválido ou expirado')
            return redirect(reverse('codigo:password-reset-request'))
        
     
        if not new_password or not confirm_password:
            messages.error(request, 'Preencha todos os campos')
            return redirect(reverse('codigo:password-reset-confirm') + f'?token={token}')
        
        if new_password != confirm_password:
            messages.error(request, 'As senhas não coincidem')
            return redirect(reverse('codigo:password-reset-confirm') + f'?token={token}')
        
        if len(new_password) < 6:
            messages.error(request, 'A senha deve ter pelo menos 6 caracteres')
            return redirect(reverse('codigo:password-reset-confirm') + f'?token={token}')
      
        try:
            admin = Admin.objects.get(email=session_email)
            admin.senha = new_password
            admin.save()
            
        
            request.session.pop('reset_token', None)
            request.session.pop('reset_email', None)
            request.session.pop('reset_link', None)
            
            print(f"DEBUG: Senha alterada com sucesso para {session_email}")
            
            messages.success(request, 'Senha alterada com sucesso! Faça login com sua nova senha.')
            return redirect(reverse('codigo:admin-login'))
        
        except Admin.DoesNotExist:
            messages.error(request, 'Usuário não encontrado')
            return redirect(reverse('codigo:password-reset-request'))
