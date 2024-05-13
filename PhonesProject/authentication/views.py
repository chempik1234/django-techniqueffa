from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from .forms import SignInForm, SignUpForm
from .models import User

DEFAULT_CONTEXT = {"title": 'Technique',
                   "title_header": "",
                   'company_phone': '+7 967 459 43 58',
                   'company_email': 'fahrazievdenis97@gmail.com',
                   'form_needs_images': False}


def main_page(request):
    data = DEFAULT_CONTEXT.copy()
    data["title_header"] = "Главная"
    return render(request, 'base.html', context=data)


class SignInView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'authentication/sign_in.html'

    def get(self, request, form=None):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        if form is None:
            form = SignInForm()
        data_context = DEFAULT_CONTEXT.copy()
        data_context["title_header"] = "Вход"
        data_context["form"] = form
        data_context['method'] = 'post'
        return Response(data_context)

    def post(self, request):
        post = SignInForm(request.POST)
        if post.is_valid():
            post.clean()
            email = post.cleaned_data.get('email')
            password = post.cleaned_data.get('password')
            user = User.objects.get(email=email, password=password)  # authenticate(request, email=password)
            if user:
                login(request, user)
                return HttpResponseRedirect("/")
        # else:
        #     messages.error(request, post.errors)
        form = post
        # data_context = DEFAULT_CONTEXT.copy()
        # data_context["title_header"] = "Вход"
        # data_context["form"] = form

        return self.get(request, form)


class SignUpView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "authentication/sign_up.html"

    def get(self, request, form=None):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        if form is None:
            form = SignUpForm()
        data_context = DEFAULT_CONTEXT.copy()
        data_context["title_header"] = "Регистрация"
        data_context["form"] = form
        data_context['method'] = 'post'
        return Response(data_context)

    def post(self, request):
        post = SignUpForm(request.POST)
        if post.is_valid():
            user = post.save()
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            form = post
            return self.get(request, form)


@login_required(login_url='/sign-in')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
