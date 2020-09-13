from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from blog.models import Post, BlogUserProfile
from blog.serializers import PostSerializer, BlogUserSerializer, BlogUserDetailsSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if type(obj) is Post:
            return obj.author.user == request.user
        elif type(obj) is BlogUserProfile:
            return obj.user == request.user


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.blog_profile)


class PostDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class BlogUserList(generics.ListAPIView):
    queryset = BlogUserProfile.objects.all()
    serializer_class = BlogUserSerializer


class BlogUserLike(generics.RetrieveUpdateAPIView):
    queryset = BlogUserProfile.objects.all()
    serializer_class = BlogUserDetailsSerializer

    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]