"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap
from rest_framework_simplejwt import views as jwt_views
from django.views.generic import TemplateView

from coreapi import views
from coreapi.views import PostListViewSet, PostDetailViewSet, \
PostsByCategoryViewSet, PostsByTagViewSet, CategoriesViewSet
from rest_framework.routers import DefaultRouter

"""
router = DefaultRouter()
router.register(r'api/post/', PostListViewSet, basename='post-list')
router.register(r'api/post/<int:post_id>', PostDetailViewSet, basename='post-detail')
#urlpatterns = router.urls
"""

post_list = PostListViewSet.as_view({
    'get': 'list',
    'post': 'post'
})

post_detail = PostDetailViewSet.as_view({
    'get': 'get',
    'put': 'put',    
    'delete': 'delete'
})

post_cat_list = PostsByCategoryViewSet.as_view({
    'get': 'list'    
})

post_tag_list = PostsByTagViewSet.as_view({
    'get': 'list'    
})

category_list = CategoriesViewSet.as_view({
    'get': 'list'    
})

urlpatterns = [
    # API
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    #path('api/blog/', views.get, name='blog'),
    #path('api/blog/<int:post_id>', views.get_blog, name='get-blog'),

    path('api/post/', post_list, name='post-list'),
    path('api/post/<int:post_id>', post_detail, name='post-detail'),

    #path('', include(router.urls)),

    #path('api/post/cat/<int:cat_id>', views.PostsByCategoryView.as_view(), name='post-list-by-cates'),
    path('api/post/cat/<int:cat_id>', post_cat_list, name='post-list-by-cates'),

    #path('api/post/tag/<int:tag_id>', views.PostsByTagView.as_view(), name='post-list-by-cates'),
    path('api/post/tag/<int:tag_id>', post_tag_list, name='post-list-by-cates'),

    #path('api/categories/', views.CategoriesView.as_view(), name='post-list-by-cates'),
    path('api/categories/', category_list, name='post-list-by-cates'),

    # Route TemplateView to serve the ReDoc template.
    #   * Provide `extra_context` with view name of `SchemaView`.
    path('api/docs/', TemplateView.as_view(
        template_name='redoc.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='redoc'),
]


