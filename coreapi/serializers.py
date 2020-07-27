from django.contrib.auth.models import User
from blog.models import Post, Tag, Category, Page, Menu
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #fields = ['url', 'username', 'email', 'is_staff']
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategoryCountSerializer(serializers.ModelSerializer):
    posts_count = serializers.IntegerField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'posts_count']

    def get_posts_count(self, obj):
        return obj.posts_count

class PostSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True, read_only=True)
    category = CategorySerializer(many=False, read_only=True)

    class Meta:
        model = Post
        #fields = '__all__'
        fields = ['id', 'title', 'slug', 'author', 
        'short_desc', 'content', 'meta_description', 
        'meta_keywords', 'cover', 'category', 'tag', 'status', 'created_on', 'updated_on']

class PostByCatgorySerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True, read_only=True)
    category = CategorySerializer(many=False, read_only=True)

    class Meta:
        model = Post
        #fields = '__all__'
        fields = ['id', 'title', 'slug', 'author', 
        'short_desc', 'content', 'meta_description', 
        'meta_keywords', 'cover', 'category', 'tag', 'status', 'created_on', 'updated_on']

class PostByTagSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=True, read_only=True)
    category = CategorySerializer(many=False, read_only=True)

    class Meta:
        model = Post
        #fields = '__all__'
        fields = ['id', 'title', 'slug', 'author', 
        'short_desc', 'content', 'meta_description', 
        'meta_keywords', 'cover', 'category', 'tag', 'status', 'created_on', 'updated_on']

class PostAddSerializer(serializers.ModelSerializer):    

    class Meta:
        model = Post
        fields = '__all__'        

class PostUpdateSerializer(serializers.ModelSerializer):    

    class Meta:
        model = Post
        fields = '__all__'
        extra_kwargs = {'title': {'required': False}, 'slug': {'required': False}, 'author': {'required': False}}        
        