from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

# Create your models here.

class Post(models.Model):
    CATEGORY_CHOICES = (
        ('bitcoin','비트코인'),
        ('altcoin','알트코인'),
        ('etc','잡담'),
    )
    author = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    title = models.TextField(max_length=40,)
    content = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("community:post_detail", args=[self.pk])

class Comment(models.Model):

    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)