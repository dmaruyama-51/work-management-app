from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path 
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from accounts.views import SignUp

app_name= 'accounts'

urlpatterns = [
    path(
        'login/', 
        LoginView.as_view(
            redirect_authenticated_user=True, 
            template_name='accounts/login.html'
        ),
        name='login'
    ),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUp.as_view(), name='signup')
]