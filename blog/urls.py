from . import views
from django.urls import include

from django.urls import path, re_path
from .feeds import LatestPostsFeed, AtomSiteNewsFeed

from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap

from .models import Post

info_dict = {
    'queryset': Post.objects.filter(status=1),
    'date_field': 'created_on',
}

urlpatterns = [
    path("feed/rss", LatestPostsFeed(), name="post_feed"),
    path("feed/atom", AtomSiteNewsFeed()),
    path("", views.PostList.as_view(), name="home"),

    path("contact", views.contact, name="contact"),
    path("contact/thanks", views.thanks, name='contact_thanks'),    
    
    # path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path("article/<slug:slug>/", views.post_detail, name="post_detail"),
    path("tag/<slug:slug>/", views.TagList.as_view(), name="tag_list"),
    #path("tag/<slug:slug>/", views.tag_list, name="tag_list"),

    path("page/<slug:slug>/", views.page_detail, name="page_detail"),

    path("category/<slug:slug>/", views.CategoryList.as_view(), name="category_list"),

    #path("about/", views.about, name="about_us"),
    #path("services/", views.services, name="services_page"),
    #path("portfolio/", views.portfolio, name="portfolio_page"),

    path('sitemap.xml', sitemap, {'sitemaps': {'blog': GenericSitemap(info_dict, priority=0.6)}},
     name='django.contrib.sitemaps.views.sitemap'),

    path("cv/me", views.mycv, name='my_cv'),
]

handler404 = 'blog.views.handler404'
