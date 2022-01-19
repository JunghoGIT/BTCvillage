from django.contrib.auth.forms import UserCreationForm
from .models import Order
from django import forms
from django.contrib.auth import get_user_model


class OrderForm(forms.ModelForm):
    position_choice =[
        ('buy','매수'),
        ('sell','매도'),
    ]
    position = forms.ChoiceField(widget=forms.Select, choices=position_choice)

    class Meta:
        model = Order
        fields = [
            'position',
            'order_price',
            'amount',
        ]

    def __init__(self, user, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_position= self.cleaned_data['position']
        cleaned_amount = self.cleaned_data['amount']
        cleaned_order_price = self.cleaned_data['order_price']
        cleaned_user = get_user_model().objects.get(pk = self.user.pk)
        user_usdt = cleaned_user.usdt
        user_wallet = cleaned_user.wallet_set.get(user_id= self.user.pk)
        user_bitcoin = user_wallet.bitcoin
        deposit = round(cleaned_amount*cleaned_order_price,2)

        if cleaned_position == 'buy':
            if deposit >= user_usdt:
                raise forms.ValidationError("구매에 필요한 USDT가 보유 USDT보다 많습니다.")
            else :
                return self.cleaned_data

        else :
            if cleaned_amount > user_bitcoin:
                raise forms.ValidationError("판매 BTC가 보유 BTC보다 큽니다.")
            return self.cleaned_data



