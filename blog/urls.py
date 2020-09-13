from django.urls import path
from blog.views import PostList, PostDetails, BlogUserList, BlogUserLike


urlpatterns = [
    path('posts/', PostList.as_view()),
    path('posts/<int:pk>', PostDetails.as_view()),
    path('bloggers/', BlogUserList.as_view()),
    path('bloggers/<int:pk>', BlogUserLike.as_view())
]