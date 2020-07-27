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
from .serializers import PostSerializer, PostAddSerializer, \
PostUpdateSerializer, CategorySerializer, CategoryCountSerializer, PostByCatgorySerializer, PostByTagSerializer
from rest_framework.decorators import api_view, permission_classes
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from django.http import Http404
from django.db.models import Count
from rest_framework.renderers import JSONRenderer
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })

class PostListViewSet(viewsets.ModelViewSet):
    """
    list:
    Return a list of all the existing posts.
    
    post:
    Create a new post instance.
    """
    
    permission_classes = [IsAuthenticated|ReadOnly]
    renderer_classes = [JSONRenderer]
    serializer_class = PostSerializer
    #pagination_class = StandardResultsSetPagination

    def list(self, request, format=None):
        #content = {'message': 'Hello, World!'}
        #return Response(content)

        posts = Post.objects.filter(status=1).order_by("-created_on")
        queryset = self.paginate_queryset(posts)
        if queryset is not None:
            serializer = PostSerializer(queryset, many=True)
            return self.get_paginated_response(serializer.data)

        # the many param informs the serializer that it will be serializing more than a single article.
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostAddSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetailViewSet(viewsets.ModelViewSet):
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
    serializer_class = PostSerializer

    def get_object(self, post_id):
        try:
            return Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, post_id):        

        posts = Post.objects.get(id=post_id)
        # the many param informs the serializer that it will be serializing more than a single article.
        serializer = PostSerializer(posts, many=False)
        return Response(serializer.data)

    def put(self, request, post_id):
        post = self.get_object(post_id)        
        serializer = PostUpdateSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id):
        post = self.get_object(post_id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostsByCategoryViewSet(viewsets.ModelViewSet):
    """
    list:
    Get Posts by Category Id.
    """
    permission_classes = [IsAuthenticated|ReadOnly]
    renderer_classes = [JSONRenderer]
    serializer_class = PostByCatgorySerializer

    def list(self, request, cat_id):
        posts = Post.objects.filter(status=1, category=cat_id).order_by("-created_on")
        queryset = self.paginate_queryset(posts)
        if queryset is not None:
            serializer = PostByCatgorySerializer(queryset, many=True)
            return self.get_paginated_response(serializer.data)
        # the many param informs the serializer that it will be serializing more than a single article.
        serializer = PostByCatgorySerializer(posts, many=True)
        return Response({"posts": serializer.data})

"""
Get Posts By Tag Id
"""

class PostsByTagViewSet(viewsets.ModelViewSet):
    """
    list:
    Get Posts by Tag Id.
    """
    permission_classes = [IsAuthenticated|ReadOnly]
    renderer_classes = [JSONRenderer]    
    serializer_class = PostByTagSerializer

    def list(self, request, tag_id):
        posts = Post.objects.filter(status=1, tag=tag_id).order_by("-created_on")
        queryset = self.paginate_queryset(posts)
        if queryset is not None:
            serializer = PostByTagSerializer(queryset, many=True)
            return self.get_paginated_response(serializer.data)
        # the many param informs the serializer that it will be serializing more than a single article.
        serializer = PostByTagSerializer(posts, many=True)
        return Response({"posts": serializer.data})

"""
Get Categories.
"""

class CategoriesViewSet(viewsets.ModelViewSet):
    """
    list:
    Get Categories.
    """
    permission_classes = [IsAuthenticated|ReadOnly]
    renderer_classes = [JSONRenderer]
    serializer_class = CategoryCountSerializer
    pagination_class = None

    def list(self, request):
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
    serializer = PostSerializer(posts, many=True)
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
        serializer = PostSerializer(posts)
        return Response(serializer.data)
    except Post.DoesNotExist: 
        return JsonResponse({'message': 'The post does not exist'}, status=status.HTTP_404_NOT_FOUND) 
"""