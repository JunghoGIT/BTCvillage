from django.shortcuts import render, redirect
from .forms import OrderForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Order,Wallet,ClosedOrder,Exchange
from django.http import JsonResponse, HttpResponse
from django.core import serializers
import json
from django import forms

# Create your views here.


@login_required
def index(request):
    form = OrderForm(request.user)
    return render(request,'btc/index.html',{
        'form' : form
    })


@login_required
def create_order_limit(request):
    order_form = OrderForm(request.user,request.POST)

    if order_form.is_valid():
        order = order_form.save(commit=False)
        order.user = request.user


        if order.position == 'buy':
            try:
                exist_order = Order.objects.get(order_price = order.order_price)
                exist_order.amount = exist_order.amount + order.amount
                extra_deposit = round(order.order_price * order.amount, 2)
                exist_order.deposit = round(order.order_price * exist_order.amount, 2)
                exist_order.save()
                orderuser = get_user_model().objects.get(pk=order.user.pk)
                orderuser.usdt = orderuser.usdt - extra_deposit
                orderuser.save()
                messages.success(request, "매수 주문 완료")
                return redirect('btc:index')
            except Order.DoesNotExist:
                order.deposit = round(order.order_price * order.amount, 2)
                order.save()
                orderuser = get_user_model().objects.get(pk=order.user.pk)
                orderuser.usdt = orderuser.usdt - order.deposit
                orderuser.save()
                messages.success(request, "매수 주문 완료")
                return redirect('btc:index')

        else :  # position ='sell'
            try :
                exist_order = Order.objects.get(order_price=order.order_price)
                exist_order.amount = exist_order.amount + order.amount
                exist_order.deposit = round(order.order_price * order.amount, 2)
                exist_order.save()
                orderuser = get_user_model().objects.get(pk=order.user.pk)
                orderuser_wallet = orderuser.wallet_set.get(user_id=orderuser.pk)
                orderuser_wallet.bitcoin = orderuser_wallet.bitcoin - order.amount
                orderuser_wallet.save()
                messages.success(request, "매도 주문 완료")
                return redirect('btc:index')
            except Order.DoesNotExist:
                orderuser = get_user_model().objects.get(pk=order.user.pk)
                orderuser_wallet = orderuser.wallet_set.get(user_id=orderuser.pk)
                order.deposit = round(order.order_price * order.amount, 2)
                order.save()
                orderuser_wallet.bitcoin = orderuser_wallet.bitcoin - order.amount
                orderuser_wallet.save()
                messages.success(request, "매도 주문 완료")
                return redirect('btc:index')
    else :
        messages.error(request,order_form.non_field_errors())
        return redirect('btc:index')



@login_required
def contract_order_limit(request):

    if request.method == 'POST':
        json_order = json.loads(request.body)
        pk = json_order.get('pk')
        contract_order = Order.objects.get(pk=pk)
        if contract_order.position == 'buy':
            new_closed_order = ClosedOrder.objects.create(
                user=contract_order.user,
                closed_price=contract_order.order_price,
                amount = contract_order.amount,
                deposit = contract_order.deposit,
                position = contract_order.position)
            new_closed_order.save()
            order_user_wallet = Wallet.objects.get(user_id= contract_order.user_id)
            if order_user_wallet.bitcoin != 0:
                temp = order_user_wallet # shot name
                order_user_wallet.average_price = round((temp.average_price * temp.bitcoin + \
                                                   contract_order.order_price * contract_order.amount)/(temp.bitcoin+contract_order.amount),2)
                order_user_wallet.bitcoin += contract_order.amount
                order_user_wallet.save()
                contract_order.delete()
                messages.success(request, "매수 주문 체결")
            else :
                order_user_wallet.average_price = contract_order.order_price
                order_user_wallet.bitcoin += contract_order.amount
                order_user_wallet.save()
                contract_order.delete()
                messages.success(request, "매수 주문 체결")
        else : # position = sell
            new_closed_order = ClosedOrder.objects.create(
                user=contract_order.user,
                closed_price=contract_order.order_price,
                amount=contract_order.amount,
                deposit=contract_order.deposit,
                position=contract_order.position)
            new_closed_order.save()
            order_user_wallet = Wallet.objects.get(user_id=contract_order.user_id)
            order_user = get_user_model().objects.get(pk=order_user_wallet.user_id)
            if (order_user_wallet.bitcoin - contract_order.amount) <= 0.001:
                order_user.usdt += contract_order.deposit
                order_user.save()
                order_user_wallet.average_price=0
                order_user_wallet.bitcoin=0
                order_user_wallet.save()
                contract_order.delete()
                messages.success(request, "매도 주문 체결")

            else :
                order_user.usdt += contract_order.deposit
                order_user.save()
                order_user_wallet.save()
                contract_order.delete()
                messages.success(request, "매도 주문 체결")

        return HttpResponse(status=201)
    else :
        return HttpResponse(status=500)

@login_required
def contract_order_market(request):
    order_form = OrderForm(request.user,request.POST)
    if request.method =='POST':
        if order_form.is_valid():
            order = order_form.save(commit=False)
            new_closed_order = ClosedOrder.objects.create(user=request.user,
                                                          closed_price =order.order_price,
                                                          amount=order.amount,
                                                          position= order.position,
                                                          deposit= round(order.order_price*order.amount,2))
            new_closed_order.save()
            if new_closed_order.position =='buy' :
                order_user = get_user_model().objects.get(pk=new_closed_order.user_id)
                order_user.usdt -= new_closed_order.deposit
                user_wallet = order_user.wallet_set.get()
                if user_wallet.bitcoin != 0:
                    user_wallet.average_price = round((user_wallet.average_price * user_wallet.bitcoin + \
                                                             new_closed_order.closed_price * new_closed_order.amount) / (
                                                                        user_wallet.bitcoin + new_closed_order.amount), 2)
                    user_wallet.bitcoin += new_closed_order.amount
                    user_wallet.save()
                    order_user.save()
                    messages.success(request, "매수 주문 체결")
                    return redirect('btc:index')
                else:
                    user_wallet.average_price = new_closed_order.closed_price
                    user_wallet.bitcoin += new_closed_order.amount
                    user_wallet.save()
                    order_user.save()
                    messages.success(request, "매수 주문 체결")
                    return redirect('btc:index')
            else :
                order_user = get_user_model().objects.get(pk=new_closed_order.user_id)
                order_user.usdt += new_closed_order.deposit
                user_wallet = order_user.wallet_set.get()
                if (user_wallet.bitcoin - new_closed_order.amount) <= 0.001 :
                    order_user.save()
                    user_wallet.average_price=0
                    user_wallet.bitcoin=0
                    user_wallet.save()
                    messages.success(request, "매도 주문 체결")
                    return redirect('btc:index')

                else :
                    order_user.save()
                    user_wallet.bitcoin -= new_closed_order.amount
                    user_wallet.save()
                    messages.success(request, "매도 주문 체결")
                    return redirect('btc:index')

        messages.error(request, order_form.non_field_errors())
        return redirect('btc:index')
    else :
        messages.success(request, "주문 실패")
        return redirect('btc:index')



@login_required
def user_order_list(request, pk):
    order_list = Order.objects.filter(user_id = pk)
    json_order = serializers.serialize('json', order_list)

    return HttpResponse(json_order, content_type="text/json-comment-filtered")

@login_required
def order_delete(request, pk):
    order = Order.objects.get(pk=pk)
    if order.position == 'buy':
        user = get_user_model().objects.get(pk=order.user_id)
        user.usdt += order.deposit
        user.save()
        order.delete()
        messages.success(request, "매수 주문 취소")
        return redirect('btc:index')
    else :
        wallet = Wallet.objects.get(user_id=order.user_id)
        wallet.bitcoin += order.amount
        wallet.save()
        order.delete()
        messages.success(request, "매도 주문 취소")
        return redirect('btc:index')

def get_exchange(request):
    exchange = serializers.serialize('json',Exchange.objects.filter(pk=1))


    return HttpResponse(exchange , content_type="text/json-comment-filtered")

@login_required
def reset_account(request, pk):
    user = get_user_model().objects.get(pk=pk)
    Order.objects.filter(user_id=pk).delete()
    Wallet.objects.filter(user_id=pk).update(bitcoin=0,average_price=0)
    user.usdt = 100000
    user.save()
    messages.success(request, "주문, 지갑, 테더 정보를 초기화 했습니다.")
    return redirect('btc:index')


def rank(request):
    user_rank = get_user_model().objects.all().order_by('-usdt')[:10]
    return render(request,'btc/rank.html',{
        'user_rank':user_rank
    })