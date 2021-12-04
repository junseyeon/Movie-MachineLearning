from django.conf import settings
from django.db import models
from django.utils import timezone


class UserInfo(models.Model):
    # id, pw, 이름, 생년월일, 좋아하는 장르, 좋아하는 영화, 싫어하는 영화, 거주 하는 나라?, 회원가입한 날짜

    id = models.CharField(max_length=50, primary_key=True)
    pw = models.CharField(max_length=50, unique=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, null=True)
    likeGenre = models.TextField()
    likeM = models.TextField()
    hateM = models.TextField()
    country = models.CharField(max_length=50)
    rate = models.CharField(max_length=20, default='user')      # 사용자 관리자 구분
    created_date = models.DateTimeField(default=timezone.now)
    # 취향 분석을 위해 추가함
    rating = models.CharField(max_length=50, null=True)
    listed_in = models.CharField(max_length=200, null=True)      # 좋아하는 장르
    director = models.CharField(max_length=200, null=True, default='N')
    cast = models.CharField(max_length=300, null=True)

    def __str__(self):
        return 'id:' + self.id + ' pw:' + self.pw

    class Meta:
        db_table = "userinfo"
