from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views import View


class SignUp(View):
    def get(self, request):
        form = UserCreationForm
        return render(request, 'accounts/signup.html')

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(self.request, user)
            return redirect('time_management:index')
        else:
            error_msg = form.errors
            form = UserCreationForm
            return render(request, 'accounts/signup.html', {'error_msg': error_msg})

