from django.shortcuts import render


# Create your views here.


def index(request):
    return render(request,'btc/index.html')



def buy_order(request):
    pass

def sell_order(request):
    pass

