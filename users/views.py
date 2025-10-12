from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import User

# ✅ 회원가입
def signup(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(email=email).exists():
            return render(request, "users/signup.html", {"error": "이미 존재하는 이메일입니다."})

        hashed_pw = make_password(password)
        User.objects.create(email=email, password=hashed_pw)

        return redirect("login")

    return render(request, "users/signup.html")

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)

            if check_password(password, user.password):  # ✅ 해시 검증
                request.session["user_email"] = user.email
                messages.success(request, f"{user.email}님 환영합니다!")
                return redirect("board_home")
            else:
                messages.error(request, "❌ 비밀번호가 올바르지 않습니다.")
        except User.DoesNotExist:
            messages.error(request, "❌ 등록되지 않은 이메일입니다.")
    return render(request, "users/login.html")

def signup_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = make_password(request.POST.get("password"))
        User.objects.create(email=email, password=password)
        messages.success(request, "회원가입이 완료되었습니다. 로그인 해주세요.")
        return redirect("login")
    return render(request, "users/signup.html")


def logout_view(request):
    request.session.flush()  # 세션 완전 초기화
    messages.success(request, "로그아웃되었습니다.")  # ✅ 메시지 설정
    return redirect("login")  # ✅ 로그인 페이지로 이동