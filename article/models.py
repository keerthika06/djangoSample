from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.

class User(AbstractUser):
    is_author = models.BooleanField(default=False)
    is_publisher = models.BooleanField(default=False)

class Article(models.Model):
    user = models.ForeignKey(User,on_delete = models.SET_NULL , null = True, blank = True)
    articleTitle = models.CharField(max_length=100)
    articleSubTitle = models.TextField()
    articleThumbnail = models.ImageField(upload_to = "images")
    articleDescription = models.TextField()
    articlestatus =models.CharField(max_length=100,default='draft')
    isreviewd = models.BooleanField(default=False)
    isrejected = models.BooleanField(default=False)
    comments = models.TextField(default='')