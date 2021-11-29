from django.shortcuts import render, redirect
from django.views.generic import View
from .models import UserInfo


class Login(View):
    def get(self, request):
        return render(request, 'Login/signin.html')

    def post(self, request):
        id = request.POST.get("id")
        pw = request.POST.get("pw")
        msg = False
        infos = UserInfo.objects.all()
        for info in infos:
            if info.id == id and info.pw == pw:
                name = info.id
                msg = True
        msg = name+"님 로그인에 성공하셨습니다"

        context = {
            'msg' : msg
        }

        # 로그인이 완료되면 넘어갈 페이지 지정 (임시로 signup.html)
        return render(request, 'main/index.html', context)


# 지금은 기능 구현 안함 admin에서 회원가입
class Signup(View):
    def get(self, request):
        return render(request, 'Login/signup.html')

    def post(self, request):
        id = request.POST.get("id")
        pw = request.POST.get("pw")

