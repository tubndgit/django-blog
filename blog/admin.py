from django.contrib import admin
from .models import Post, Comment, Tag, Contact, Category, Page, Menu

from django_summernote.admin import SummernoteModelAdmin

class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'status', 'view_count', 'created_on')
    list_filter = ('status', 'created_on')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

    summernote_fields = ('content', 'short_desc')

class PageAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'status', 'created_on')
    list_filter = ('status', 'created_on')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

    summernote_fields = ('content',)

class TagAdmin(SummernoteModelAdmin):
    list_display = ('name', 'slug')
    list_filter = ('created_on',)
    search_fields = ['name']    
    prepopulated_fields = {'slug': ('name',)}

    #summernote_fields = ('name',)

class CategoryAdmin(SummernoteModelAdmin):
    list_display = ('name', 'slug')
    list_filter = ('created_on',)
    search_fields = ['name']    
    prepopulated_fields = {'slug': ('name',)}

class ContactAdmin(SummernoteModelAdmin):
    list_display = ('contact_name', 'contact_email')
    list_filter = ('created_on',)
    search_fields = ['contact_name']    
    #prepopulated_fields = {'slug': ('name',)}

class MenuAdmin(SummernoteModelAdmin):
    list_display = ('title', 'url', 'order', 'status', 'created_on')
    list_filter = ('order', 'created_on',)
    search_fields = ['title']        

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Menu, MenuAdmin)

