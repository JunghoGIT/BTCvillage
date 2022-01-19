from django.urls import path,include
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.community_index , name='community_index'),
    path('post/detail/<int:pk>', views.post_detail, name='post_detail'),
    path('post/<int:pk>/comment/create', views.comment_create, name='comment_create'),
    path('post/create/',views.post_create, name='post_create')
]
