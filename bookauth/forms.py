from django import forms
from django.contrib.auth import get_user_model
from .models import CaptchaModel

User = get_user_model()


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=2, error_messages={
        'require': "Please enter your username.",
        "max_length": 'The length of username should be between 2 and 20 characters.',
        "min_length": 'The length of username should be between 2 and 20 characters.'
    })
    email = forms.EmailField(
        error_messages={'require': "Please enter your email address.", 'invalid': "The email address is invalid."})
    captcha = forms.CharField(max_length=4, min_length=4)
    password = forms.CharField(max_length=20, min_length=6)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha')
        email = self.cleaned_data.get('email')
        captcha_model = CaptchaModel.objects.filter(email=email, captcha=captcha).first()
        if not captcha_model:
            raise forms.ValidationError("Verification code is unsuitable.")
        captcha_model.delete()
        return captcha


class LoginForm(forms.Form):
    email = forms.EmailField(
        error_messages={'require': "Please enter your email address.", 'invalid': "The email address is invalid."})
    password = forms.CharField(max_length=20, min_length=6)
    remember = forms.IntegerField(required=False)
