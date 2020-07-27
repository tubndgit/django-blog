from django.views import generic
from .models import Post, Tag, Category, Page, Menu
from .forms import CommentForm, ContactForm
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings

from django.core.mail import BadHeaderError, EmailMessage
from django.http import HttpResponse
from django.db.models import Count
from bs4 import BeautifulSoup

import logging
logger = logging.getLogger("mylogger")

_SITE_NAME = getattr(settings, "SITE_NAME", '')
_AUTHOR = getattr(settings, "AUTHOR", '')

def get_menus():
    menus = Menu.objects.filter(status=1).order_by("order")
    return menus

def get_categories():
    categories = Category.objects.all().annotate(posts_count=Count('post_category')).filter(status=1, posts_count__gt=0)
    return categories

def get_1st_image(post):
    img_link = ''
    media_path = getattr(settings, "MEDIA_URL", '')
    img_path = post.cover
    if not img_path:
        content = post.content        
        tree = BeautifulSoup(content)
        img_links = tree.find_all('img')
        if img_links:
            img_link = img_links[0].get('src')
    else:        
        img_link = '{}{}'.format(media_path, img_path)
    return img_link

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = getattr(settings, "PAGE_SIZE", 5)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menus = get_menus()                           
        context["menus"] = menus  
        categories = get_categories()  
        context["categories"] = categories    
        context["author"] = _AUTHOR
        return context


# class PostDetail(generic.DetailView):
#     model = Post
#     template_name = 'post_detail.html'


def post_detail(request, slug):
    template_name = "post_detail.html"    
    post = get_object_or_404(Post, slug=slug)

    # View count
    post.view_count = post.view_count + 1
    post.save()

    comments = post.comments.filter(active=True).order_by("-created_on")
    new_comment = None
    # Comment posted
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(
        request,
        template_name,
        {
            "post": post,
            "comments": comments,
            "new_comment": new_comment,
            "comment_form": comment_form,
            "menus": get_menus(),
            "categories": get_categories(),
            'site_name': _SITE_NAME,
            'main_image': get_1st_image(post),
            'author': _AUTHOR,
            'baseurl': request.build_absolute_uri()
        },
    )

class TagList(generic.ListView):
    model = Post
    template_name = "tag_list.html"
    paginate_by = getattr(settings, "PAGE_SIZE", 5)
    
    def get_queryset(self, **kwargs):        
        slug = self.kwargs.get('slug', '')
        print(slug, self.kwargs)        
        queryset = Post.objects.filter(status=1, tag__slug=slug).order_by("-created_on")
        return queryset    

    def get_context_data(self, **kwargs):
        slug = self.kwargs.get('slug', '')

        context = super().get_context_data(**kwargs)

        Tags= Tag.objects.filter(slug=slug)        
        
        if Tags:
            context['page_title'] = '#{}'.format(Tags[0].name)
        else:
            context['page_title'] = 'Not found'

        menus = get_menus()                       
        context["menus"] = menus
        categories = get_categories()  
        context["categories"] = categories
        context["author"] = _AUTHOR

        return context  

class CategoryList(generic.ListView):
    model = Post
    template_name = "tag_list.html"
    paginate_by = getattr(settings, "PAGE_SIZE", 5)
    
    def get_queryset(self, **kwargs):        
        slug = self.kwargs.get('slug', '')
        print(slug, self.kwargs)        
        queryset = Post.objects.filter(status=1, category__slug=slug).order_by("-created_on")
        return queryset    

    def get_context_data(self, **kwargs):
        slug = self.kwargs.get('slug', '')

        context = super().get_context_data(**kwargs)

        Categories= Category.objects.filter(slug=slug)        
        
        if Categories:
            context['page_title'] = '{}'.format(Categories[0].name)
        else:
            context['page_title'] = 'Not found'

        menus = get_menus()                       
        context["menus"] = menus
        categories = get_categories()  
        context["categories"] = categories
        context["author"] = _AUTHOR

        return context  

def handler404(request, exception):
    menus = get_menus()
    categories = get_categories()
    return render(request, '404.html', locals())

def contact(request):
    new_contact = None
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            new_contact = form.save()
            contact_name = form.cleaned_data['contact_name']
            contact_email = form.cleaned_data['contact_email']
            content = form.cleaned_data['content']
            try:
                email = EmailMessage(contact_name,
                                    content,
                                    contact_email,
                                    [getattr(settings, "ADMIN_EMAIL", '')], #change to your email
                                     reply_to=[contact_email],
                                   )
                email.send()
            #except BadHeaderError:
            #    return HttpResponse('Invalid header found.')
            except Exception as e:
                pass

            return redirect('./contact/thanks')
    return render(request, 'contact.html', {
            'contact_form': form, 
            'page_title': 'Contact Us',
            "menus": get_menus(),
            "categories": get_categories()
        })


def thanks(request):
    return render(request, 'thanks.html', {"menus": get_menus(), "categories": get_categories()})

def about(request):
    return render(request, 'about.html', {
        'page_title': 'About Us', 
        "menus": get_menus(), 
        "categories": get_categories()
        })

def services(request):
    return render(request, 'services.html', 
        {
            'page_title': 'Services',
            "menus": get_menus(),
            "categories": get_categories()
        }
    )

def portfolio(request):
    return render(request, 'portfolio.html', 
        {
            'page_title': 'Portfolio',
            "menus": get_menus(),
            "categories": get_categories()
        }
    )

def page_detail(request, slug):
    template_name = "page_detail.html"    
    page = get_object_or_404(Page, slug=slug, status=1)
    
    return render(
        request,
        template_name,
        {
            "page": page,   
            "menus": get_menus(),
            "categories": get_categories()     
        },
    )


def mycv(request):
    return render(request, 'curriculum_vitae.html')