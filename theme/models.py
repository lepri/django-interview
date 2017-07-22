from django.db import models
from .validators import validate_date_uploaded


class Theme(models.Model):
    """ Theme model
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Video(models.Model):
    """ Video model
    """

    title = models.CharField(max_length=100)
    date_uploaded = models.DateField(validators=[validate_date_uploaded])
    views = models.IntegerField()
    themes = models.ManyToManyField(Theme)

    def __str__(self):
        return self.title


class Thumb(models.Model):
    """ Thumb model
    """
    is_positive = models.BooleanField(default=True)
    time = models.DateTimeField(auto_now_add=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE,)

    def __str__(self):
        return self.video.title


class Comment(models.Model):
    """ Comment model
    """
    is_positive = models.BooleanField(default=True)
    time = models.DateTimeField(auto_now_add=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE,)

    def __str__(self):
        return self.video.title
