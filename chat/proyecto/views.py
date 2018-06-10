# -*- coding: cp1252 -*-
# -*- coding: 850 -*-
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import contrib
from django.contrib.auth import login, authenticate
from django.shortcuts import render

from django.http import HttpResponse
from django.core.files.storage import default_storage

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.fields.files import FieldFile
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.template import loader
from requests import auth
from django.contrib.auth.models import User as Us


from .forms import ContactForm, FilesForm, ContactFormSet, SignUpForm
from .models import Post, User
import datetime

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from . import rsa
from django.core.mail import send_mail

global USUARIO


def index(request):
    return render(request, 'profile.html')


def inicioSesion(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        global USUARIO
        USUARIO = User.objects.get(username=username)
        latest_question_list = Post.objects.filter(usuario=USUARIO)
        template = loader.get_template('proyecto/perfil.html')
        context = {
            'latest_question_list': latest_question_list,
        }
        return HttpResponse(template.render(context, request))

    else:
        return render(request, 'profile.html')


def message(request):
    return render(request, 'proyecto/messages.html')


class DefaultFormView(FormView):
    template_name = 'proyecto/form.html'
    form_class = ContactForm


def enviarMensaje(request):
    titulo = request.POST['titulo']
    texto = request.POST['message']
    global USUARIO
    user = USUARIO
    mensaje = rsa.encriptar(texto, user.clavepublica_d , user.clavepublica_e)
   
    m = Post(texto=mensaje, titulo=titulo, usuario=USUARIO, date=datetime.datetime.now())
    m.save()
    latest_question_list = Post.objects.filter(usuario=USUARIO)
    template = loader.get_template('proyecto/perfil.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))



def signup(request):
    return render(request, 'proyecto/signup.html')


def descifrar(request, id):
    post = Post.objects.get(id=id)
    global USUARIO
    user = USUARIO
    text = rsa.desencriptar(post.texto,user.clavepublica_d ,user.clavepublica_e, user.phi )
    string = "El texto desencriptado es: \n" + text
    messages.info(request, string, )
    latest_question_list = Post.objects.filter(usuario=USUARIO)
    template = loader.get_template('proyecto/perfil.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))


def registro(request):
    username = request.POST['new_username']
    password = request.POST['new_password']
    email = request.POST['new_email']

    claves = rsa.generarClavePublica()

    u = User(username=username, password=password, email=email, clavepublica_d=claves[0], clavepublica_e=claves[1],
             phi=claves[2])
    u.save()

    us =  Us.objects.create_user(username, email, password)
    us.set_password(password)
    us.save()

    #email_sender = 'helenaridocci@gmail.com'

    #send_mail('Claves','La clave publica es:' + '\n'+  'La clave privada es:',email_sender,[email],fail_silently=False,)

    text_claves = 'Tu claves publicas son \n' + 'n:' + str(claves[0]) + '\ne:' + str(claves[1])

    messages.info(request, text_claves)
    return HttpResponse(render(request, 'profile.html'))
