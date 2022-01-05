from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

class SignupForm(UserCreationForm):
    class Meta:
        model= get_user_model()
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'nickname',
        ]
    def clean_nickname(self):
        nickname= self.cleaned_data['nickname']
        if get_user_model().objects.filter(nickname=nickname).exists():
            raise forms.ValidationError("사용중인 닉네임 입니다.")
        else :
            return nickname


