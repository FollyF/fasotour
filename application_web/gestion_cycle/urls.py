
from django.contrib.auth import views as auth_views
from django.urls import path

from .views import *

urlpatterns = [
    #index
    path('', home, name='home'),
    path('sites_touristiques/', sites_touristiques, name='sites_touristiques'),
    path('detail_site/<int:site_id>/', detail_site, name='detail_site'),
    path('circuits/', circuits, name='circuits'),
    path('circuits/<int:circuit_id>/', detail_circuit, name='detail_circuit'),
    path('connexion/', connexion, name='connexion'),
    path('inscription/',inscription, name='inscription'),
    path('mes_reservations/', mes_reservations, name='mes_reservations'),
    path('circuit/<int:circuit_id>/reserver/',reserver_circuit, name='reserver_circuit'),
    path('deconnexion/', deconnexion, name='deconnexion'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
]

