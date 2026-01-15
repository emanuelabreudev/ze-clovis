"""
Rotas de URL do sistema
"""
from django.urls import path
from codigo.views import (
    Home,
    AdminLogin,
    AdminHome,
    AdminSetup,
    AdminUserRegister,
    AdminLog,
    AdminReport,
    PasswordResetRequest,
    PasswordResetSent,
    PasswordResetConfirm,
    UserArrive,
    UserArriveLogin,
    UserArriveToken,
    UserDepart,
    UserDepartPrice
)

app_name = 'codigo'

urlpatterns = [
   
    path('', Home.as_view(), name='home'),
    

    path('admin/login/', AdminLogin.as_view(), name='admin-login'),
    path('admin/home/', AdminHome.as_view(), name='admin-home'),
    path('admin/configuracao/', AdminSetup.as_view(), name='admin-config'),
    path('admin/registro/', AdminUserRegister.as_view(), name='admin-user-register'),
    path('admin/log/', AdminLog.as_view(), name='admin-log'),
    path('admin/relatorio/', AdminReport.as_view(), name='admin-report'),
    
    
    path('admin/redefinir-senha/', PasswordResetRequest.as_view(), name='password-reset-request'),
    path('admin/redefinir-senha/enviado/', PasswordResetSent.as_view(), name='password-reset-sent'),
    path('admin/redefinir-senha/confirmar/', PasswordResetConfirm.as_view(), name='password-reset-confirm'),

  
    path('entrada/', UserArrive.as_view(), name='user-arrive'),
    path('entrada/login/', UserArriveLogin.as_view(), name='user-login'),
    path('entrada/ficha/', UserArriveToken.as_view(), name='user-token'),

   
    path('saida/', UserDepart.as_view(), name='user-depart'),
    path('saida/pagamento/', UserDepartPrice.as_view(), name='user-price'),
]