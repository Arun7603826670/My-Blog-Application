from django.contrib import admin
from .models import Category, Post, ContactMessage, AboutPage, Subscriber

# Admin for Post model
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    prepopulated_fields = {"slug": ("title",)}

# Admin for ContactMessage model
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at')
    search_fields = ['name', 'email']
    list_filter = ['submitted_at']

# Register other models
admin.site.register(Category)
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(AboutPage)
admin.site.register(Subscriber)
