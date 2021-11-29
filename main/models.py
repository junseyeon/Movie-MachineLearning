from django.db import models


class MovieModel(models.Model):
    show_id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=30)
    title = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    cast = models.TextField()
    country = models.CharField(max_length=200)
    release_year = models.IntegerField(null=True)
    rating = models.CharField(max_length=30)
    duration = models.CharField(max_length=60)
    listed_in = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.show_id + self.title

    class Meta:
        db_table ='moviemodel'



