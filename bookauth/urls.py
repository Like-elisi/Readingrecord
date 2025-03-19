from django.urls import path
from . import views
app_name = 'bookauth'

urlpatterns = [
    path('login',views.booklogin,name='login'),
    path('register',views.register,name='register'),
    path('captcha',views.send_email_captcha,name='email_captcha'),
    path('logout',views.booklogout,name='logout'),
]