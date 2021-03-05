from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.forms import AuthenticationForm
# authenticate : 인증 기능
# login : 로그인 기능
# redirect : 로그인을 했을 시 어떤 페이지로 보낼지에 관한 기능
# render : templates을 렌더링하는 기능
# logout : 로그아웃 기능
from .forms import SignupForm


def signup(request):
    # 요청이 POST일 경우 forms.py에 정의한 SignupForm을 load
    # Form의 값이 제대로 채워졌을 경우 저장 후 로그인페이지로 리다이렉트
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            return redirect('accounts:login')
    # POST가 아닐 경우 회원가입 페이지 다시 렌더링
    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {
        'form': form,
    })


def login_check(request):
    if request.method == 'POST':
        # POST 요청으로 받은 계정과 비밀번호를 가지고 유저판단
        # 유저면 로그인 후 URL('/')로 이동
        form = AuthenticationForm(request, request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("/")

    else:
        form = AuthenticationForm()
    # POST요청이 아니라면 로그인 페이지 다시 렌더링
    return render(request, 'accounts/login.html', {"form": form})


def logout(request):
    django_logout(request)
    return redirect("/")
