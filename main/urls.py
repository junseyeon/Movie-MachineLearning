from django.urls import path, include
from . import views

app_name = 'main'
# 경로, views 함수명 , name은 나주중에 login이란 이름의 key로 사용
urlpatterns = [
     # 아래건 /main으로 들어갔을 때 바로 뜨는 경로
     # path('', views.index, name="index"),  # 좋아하는 영화만 따로 값을 받는 경로였음.

     # ISSUE / path의 매칭되는 앞에 형식만 보고서 맞으면 바로 들어가 버림... id랑 상관없이... 그래서 every/로 경로 바꿔줌//

     path('every/<slug:nameid>/', views.result, name="result"),  # 영화만

     path('<slug:u_id>/', views.using, name="using"),  # 사용자

     # path('', views.result, name="result"),

     path('manager/', views.manager, name="manager"),

     path('csv/', views.csvToModel, name="csv"),

]
