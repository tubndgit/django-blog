from django.shortcuts import render

# Create your views here.
"""
Blog API
"""
from blog.models import Post, Tag, Category, Page, Menu
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from django.contrib.auth.models import User
from .serializers import BlogSerializer, BlogAddSerializer, BlogUpdateSerializer, CategorySerializer, CategoryCountSerializer
from rest_framework.decorators import api_view, permission_classes
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from django.http import Http404
from django.db.models import Count
from rest_framework.renderers import JSONRenderer

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class PostListView(APIView):
    """
    get:
    Return a list of all the existing posts.

    **Example request**:

        GET  /api/post/

    **Example response**:

        {
            "posts": [
                {
                    "id": 6,
                    "title": "testing add post via api 044c775e-bffe-11ea-8138-6045cb8247e2",
                    "slug": "testing-add-post-via-api-044c775e-bffe-11ea-8138-6045cb8247e2",
                    "author": 1,
                    "short_desc": "",
                    "content": "Update post",
                    "meta_description": "Update meta description",
                    "meta_keywords": "",
                    "cover": null,
                    "category": {
                        "id": 2,
                        "name": "Uncategory",
                        "slug": "uncategory",
                        "created_on": "2020-05-14T03:39:55.614445Z",
                        "updated_on": "2020-05-14T03:39:55.614445Z",
                        "status": 0
                    },
                    "tag": [
                        {
                            "id": 2,
                            "name": "scrapy",
                            "slug": "scrapy",
                            "created_on": "2020-05-09T04:01:00.909847Z",
                            "updated_on": "2020-05-09T04:01:00.909847Z"
                        },
                        {
                            "id": 3,
                            "name": "web scraping",
                            "slug": "web-scraping",
                            "created_on": "2020-05-09T04:01:20.546734Z",
                            "updated_on": "2020-05-09T04:01:20.546734Z"
                        }
                    ],
                    "status": 0,
                    "created_on": "2020-07-07T03:00:30.505819Z",
                    "updated_on": "2020-07-07T03:27:04.529211Z"
                },
                {
                    ..
                },
                {
                    ..
                }
            ]
        }

    post:
    Create a new post instance.

    **Example request**:

        POST  /api/post/

    **Example response**:

        {
            
        }
    """

    permission_classes = [IsAuthenticated|ReadOnly]
    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):
        #content = {'message': 'Hello, World!'}
        #return Response(content)

        posts = Post.objects.filter(status=1).order_by("-created_on")
        # the many param informs the serializer that it will be serializing more than a single article.
        serializer = BlogSerializer(posts, many=True)
        return Response({"posts": serializer.data})

    def post(self, request):
        serializer = BlogAddSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetailView(APIView):
    """
    get:
    Get the given post id.

    put:
    Update an existing post.

    delete:
    Delete a post instance.
    """
    permission_classes = [IsAuthenticated|ReadOnly]
    renderer_classes = [JSONRenderer]

    def get_object(self, post_id):
        try:
            return Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, post_id):        

        posts = Post.objects.get(id=post_id)
        # the many param informs the serializer that it will be serializing more than a single article.
        serializer = BlogSerializer(posts, many=False)
        return Response(serializer.data)

    def put(self, request, post_id):
        post = self.get_object(post_id)        
        serializer = BlogUpdateSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id):
        post = self.get_object(post_id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostsByCategoryView(APIView):
    """
    get:
    Get Posts by Category Id.
    """
    permission_classes = [IsAuthenticated|ReadOnly]
    renderer_classes = [JSONRenderer]

    def get(self, request, cat_id):
        posts = Post.objects.filter(status=1, category=cat_id).order_by("-created_on")
        # the many param informs the serializer that it will be serializing more than a single article.
        serializer = BlogSerializer(posts, many=True)
        return Response({"posts": serializer.data})

"""
Get Posts By Tag Id
"""

class PostsByTagView(APIView):
    """
    get:
    Get Posts by Tag Id.
    """
    permission_classes = [IsAuthenticated|ReadOnly]
    renderer_classes = [JSONRenderer]

    def get(self, request, tag_id):
        posts = Post.objects.filter(status=1, tag=tag_id).order_by("-created_on")
        # the many param informs the serializer that it will be serializing more than a single article.
        serializer = BlogSerializer(posts, many=True)
        return Response({"posts": serializer.data})

"""
Get Categories.
"""

class CategoriesView(APIView):
    """
    get:
    Get Categories.
    """
    permission_classes = [IsAuthenticated|ReadOnly]
    renderer_classes = [JSONRenderer]

    def get(self, request):
        categories = Category.objects.all().annotate(posts_count=Count('post_category')).filter(status=1, posts_count__gt=0)
                        
        serializer = CategoryCountSerializer(categories, many=True)
        return Response({"categories": serializer.data})

"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get(request):
    ""
    some text
    ""
    #content = {'message': 'Hello, World!'}
    #return Response(content)

    posts = Post.objects.all()        
    # the many param informs the serializer that it will be serializing more than a single article.
    serializer = BlogSerializer(posts, many=True)
    return Response({"posts": serializer.data})

@api_view(['GET'])
def get_blog(request, post_id):
    ""
    some text
    ""
    #content = {'message': 'Hello, World!'}
    #return Response(content)

    try:
        posts = Post.objects.get(id=post_id)        
        # the many param informs the serializer that it will be serializing more than a single article.
        serializer = BlogSerializer(posts)
        return Response(serializer.data)
    except Post.DoesNotExist: 
        return JsonResponse({'message': 'The post does not exist'}, status=status.HTTP_404_NOT_FOUND) 
"""