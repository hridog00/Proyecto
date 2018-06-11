from django.conf.urls import url, include
from django.urls import path

from .import views

urlpatterns = [

    path('', views.index, name='index'),
    path('inicioSesion', views.inicioSesion, name='inicioSesion'),
    path('perfil', views.perfil, name='perfil'),

    url(r'^signup', views.signup, name='signup'),

    path('sendMessage', views.enviarMensaje, name='perfilnMessge'),
    url('registro', views.registro, name='registro'),

    # url(r'^accounts/login$', 'django.contrib.auth.views.login'),
    url(r'^form$', views.DefaultFormView.as_view(), name='form_default'),
    url(r'^message', views.message, name='escribe_mensajet'),
    path('descifrar/<int:id>/', views.descifrar ,name="descifrar"),


]