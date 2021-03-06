from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import View
from .models import UserInfo
from main.models import Movie
from django.urls import reverse
from datetime import datetime


class Login(View):

    def get(self, request):

        # db에 있는 title값 만 가져오기
        titles = Movie.objects.values('title')
        context = {
            "titles": titles
        }
        return render(request, 'Login/signin.html', context=context)

    def post(self, request):
        u_id = request.POST.get("id")
        pw = request.POST.get("pw")
        name = request.POST.get("name")
        msg = False      # 계정 유/무 파악
        root = False    # 관리자 계정인지 파악

        try:     # 비회원 영화 추천
            row = Movie.objects.get(title=name)
            nameid = row.show_id
        except Movie.DoesNotExist:
            print("영화 안골랐음")

        infos = UserInfo.objects.all()
        for info in infos:
            if info.id == u_id and info.pw == pw:
                msg = True
                if info.rate == 'mgr' or info.rate =='own':
                    root = True
                break
            else:
                print('로그인 정보 없음')         # 나중에 alert_message 추가

        if root:
            print('adsfdf')
            return HttpResponseRedirect(reverse('main:manager'))
        elif msg:
            print("로그인 했을 때 취향 분석")
            return HttpResponseRedirect(reverse('main:using', args=(u_id, )))         # 로그인
        elif nameid:
            print("비회원 영화 추천해줌")
            return HttpResponseRedirect(reverse('main:result', args=(nameid, )))       # 비회원 영화 추천
            


        # context = {
        #     'id': id,
        #     'demo': demo
        # }  # 넘기는건 딕셔너리로 한번에 하고 받는 페이지에서 key별로 출력

        # 이렇게 render하면 main/views.py로 안가지고 바로 index.html로 넘어가져서 문제.
        # return render(request, 'Login/signin.html', context)      #uri 뒤에 name붙여서 가야 될 듯 (context필요 x)
        # return redirect('main/')


# 지금은 기능 구현 안함 admin에서 회원가입
class Signup(View):

    def get(self, request):
        return render(request, 'Login/signup.html')

    def post(self, request):
        id = request.POST.get("id")
        pw = request.POST.get("pw")

        #fb = UserInfo(id= id, pw= pw, birth_date=bd, likeGenre= lg, likeM=lm, hateM=hm, country= country, created_date= datetime.now())
        #fb.save()
