from django.urls import path, include
from . import views

app_name = 'main'
# 경로, views 함수명 , name은 나주중에 login이란 이름의 key로 사용
urlpatterns = [
     # 아래건 /main으로 들어갔을 때 바로 뜨는 경로
     # path('', views.index, name="index"),  # 좋아하는 영화만 따로 값을 받는 경로였음.

     path('<slug:u_id>/<slug:nameid>/', views.result, name="result"),
     # path('', views.result, name="result"),

     path('admin/', views.administrator, name="admin"),

     path('csv/', views.csvToModel, name="csv"),

    # path('index/<int:id>', views.index, name="analysis"),
]
