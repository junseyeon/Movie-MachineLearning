from django.db import models


class MovieModel(models.Model):
    show_id = models.TextField()
    type = models.TextField()
    title = models.TextField()
    director = models.TextField()
    cst = models.TextField()
    country = models.CharField(max_length=50)
    release_year = models.IntegerField
    rating = models.CharField(max_length= 30)
    duration = models.CharField(max_length=60)
    listed_in = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.show_id
