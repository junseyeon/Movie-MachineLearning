
from django.conf import settings
from django.db import models
from django.utils import timezone


class Consumer(models.Model):
    # id, pw 이름, 생년월일, 좋아하는 장르, 좋아하는 영화, 싫어하는 영화, 거주 하는 나라?, 회원가입한 날짜

    id = models.CharField(max_length=50, primary_key=True)
    pw = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    birth_date = models.DateField(blank=True, null=True)
    likeGenre = models.TextField()
    likeM = models.TextField()
    hateM = models.TextField()
    country = models.CharField(max_length=50)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
