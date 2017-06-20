from django.contrib import admin
from warmth.models import Category, Page, UserProfile

class PageAdmin(admin.ModelAdmin) :
    list_display = ['title','category','url','views']

class CategoryAdmin(admin.ModelAdmin) :
    prepopulated_fields = {'slug':('name',)}
    list_display = ['name','views','likes','slug']

class UserProfileAdmin(admin.ModelAdmin) :
    list_display = ['website','picture']



admin.site.register(Category,CategoryAdmin)
admin.site.register(Page,PageAdmin)
admin.site.register(UserProfile,UserProfileAdmin)
# Register your models here.
