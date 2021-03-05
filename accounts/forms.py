from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Profile
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    username = forms.CharField(label='사용자명', widget=forms.TextInput(attrs={
        'pattern': '[a-zA-Z0-9]+',
        'title': '특수문자, 공백 입력불가',
    }))

    nickname = forms.CharField(label='닉네임')
    picture = forms.ImageField(label='프로필 사진', required=False)

    # 프로필 사진은 optional

    # Meta : 모델 단위의 옵션 설정 가능
    class Meta(UserCreationForm.Meta):
        # fields 변수에 회원가입 폼에서 보여줄 필드들을 설정
        fields = UserCreationForm.Meta.fields + ('email',)

    # 유효성 검사 : 입력한 값이 이미 존재하는 값인지 확인하는 메소드
    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        if Profile.objects.filter(nickname=nickname).exists():
            raise forms.ValidationError('이미 존재하는 닉네임 입니다.')
        return nickname

    def clean_email(self):
        email = self.cleaned_data.get('email')
        User = get_user_model()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('사용중인 이메일 입니다.')
        return email

    def clean_picture(self):
        picture = self.cleaned_data.get('picture')
        if not picture:
            picture = None
        return picture

    # user 모델과 입력된 값들을 바탕으로 프로필을 만들기
    def save(self):
        user = super().save()
        Profile.objects.create(
            user=user,
            nickname=self.cleaned_data['nickname'],
            picture=self.cleaned_data['picture'],
        )
        return user
