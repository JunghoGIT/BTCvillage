from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as Sign_login,logout as auth_logout
from .forms import SignupForm, CustomLoginForm
from btc.models import Wallet
# Create your views here.


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            signed_user = form.save()
            Sign_login(request, signed_user)
            user_wallet =Wallet.objects.create(user = signed_user, average_price=0,bitcoin=0)
            user_wallet.save()
            return redirect('btc:index')
    else :
        form = SignupForm()
    return render(request, 'accounts/signup_form.html',{
            'form': form
        })

class CustomLoginview(LoginView):
    form_class = CustomLoginForm


login = CustomLoginview.as_view(template_name='accounts/login_form.html')

def logout(request):
    auth_logout(request)
    return redirect('btc:index')
