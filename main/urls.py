from django.urls import path, include
from . import views

# 경로, views 함수명 , name은 나주중에 login이란 이름의 key로 사용
urlpatterns = [
     # 아래건 /main으로 들어갔을 때 바로 뜨는 경로
      path('', views.index, name="index"),
      path('csv/', views.csvToModel, name="csv"),
    # path('index/<int:id>', views.index, name="analysis"),
]
