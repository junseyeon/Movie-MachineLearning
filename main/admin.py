from django.contrib import admin
from .models import MovieModel

# models.py에 등록된 클래스(테이블?)들을 여기서 추가해야 관리자화면에서 볼수 있음
admin.site.register(MovieModel)
