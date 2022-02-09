from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms

class SignupForm(UserCreationForm):
    username = forms.CharField(label='아이디')
    email = forms.EmailField(label='이메일')
    first_name = forms.CharField(label='이름')
    last_name = forms.CharField(label='성')
    nickname = forms.CharField(label='닉네임')

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = "비밀번호"
        self.fields['password2'].label = "비밀번호 확인"

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


class CustomLoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': (
            "비밀번호나 이메일이 올바르지 않습니다. 다시 확인해 주세요."
        ),
    }

    def __init__(self, request=None, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = '아이디'
        self.fields['password'].label = '비밀번호'