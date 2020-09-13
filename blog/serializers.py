from rest_framework import serializers
from blog.models import Post, BlogUserProfile
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model


User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    likes = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='username'
     )
    class Meta:
        model = Post
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class ShortPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'id']


class BlogUserSerializer(serializers.ModelSerializer):
    likes = ShortPostSerializer(many=True, read_only=True)
    posts = ShortPostSerializer(many=True, read_only=True)
    class Meta:
        model = BlogUserProfile
        fields = ['user', 'likes', 'posts']
        

class BlogUserDetailsSerializer(serializers.ModelSerializer):
    likes = serializers.PrimaryKeyRelatedField(many=True, queryset=Post.objects.all())
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = BlogUserProfile
        fields = ['likes', 'posts']

        
# this should't be here, but because we don't do anything, I'll keep it here anyway
class NewUserCreateSerializer(UserCreateSerializer):
    def validate(self, attrs):
        email = attrs.get('email')
        if False:
            raise serializers.ValidationError(
                {"email": "Hunter.io hates you!"}
        )
        return super().validate(attrs)