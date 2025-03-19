from django.shortcuts import render,redirect,reverse
from django.http.response import JsonResponse
import string
import random
from django.core.mail import send_mail
from .models import CaptchaModel
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm , LoginForm
from django.contrib.auth import get_user_model,login,logout


User = get_user_model()

@require_http_methods(['GET','POST'])
def booklogin(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                login(request, user)
                if not remember:
                    request.session.set_expiry(0)
                return redirect('/')
            else:
                form.add_error('email','email or password is incorrect')
                return render(request, 'login.html',context={'form':form})



@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, email=email, password=password)
            return redirect(reverse('bookauth:login'))
        else:
            print(form.errors)
            return redirect(reverse('bookauth:register'))





def send_email_captcha(request):
    email = request.GET.get('email')
    if not email:
        return JsonResponse({"code": 400, "message": 'must provide email'})
    captcha = "".join(random.sample(string.digits, 4))
    print(captcha)
    CaptchaModel.objects.update_or_create(email=email,defaults={'captcha':captcha})
    send_mail("Verification code", message=f"Your register verification code is {captcha}", recipient_list=[email],
              from_email=None)
    return JsonResponse({"code": 200, "message": "Send successfully"})


def booklogout(request):
    logout(request)
    return redirect('/')