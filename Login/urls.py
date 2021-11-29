from django.urls import path, include
from . import views

# 경로, views 함수명 , name은 나주중에 login이란 이름의 key로 사용
urlpatterns = [
    path('', views.Login.as_view(), name='login'),
    path('signup/', views.Signup.as_view(), name='signup'),
]
