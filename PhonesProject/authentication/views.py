from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from .forms import SignInForm, SignUpForm
from .models import User


def profile_view(request):
    data = {"title_header": "Профиль"}
    return render(request, 'authentication/profile.html', context=data)


class SignInView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'authentication/sign_in.html'

    def get(self, request, form=None):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        if form is None:
            form = SignInForm()
        data_context = {"title_header": "Вход", "form": form, 'method': 'post'}
        return Response(data_context)

    def post(self, request):
        post = SignInForm(request.POST)
        if post.is_valid():
            post.clean()
            email = post.cleaned_data.get('email')
            password = post.cleaned_data.get('password')
            user = User.objects.get(email=email)  # authenticate(request, email=password)
            if user and user.check_password(password):
                login(request, user)
                return HttpResponseRedirect("/")
        form = post

        return self.get(request, form)


class SignUpView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "authentication/sign_up.html"

    def get(self, request, form=None):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        if form is None:
            form = SignUpForm()
        data_context = {"title_header": "Регистрация", "form": form, 'method': 'post'}
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
