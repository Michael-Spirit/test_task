from django.contrib import admin
from .models import Product, Comment


class ProductAdmin(admin.ModelAdmin):
    view_on_site = True
    list_display = ('name', 'slug', 'price', 'created_at', 'modified_at')
    exclude = ('slug', )


class CommentAdmin(admin.ModelAdmin):
    view_on_site = True
    list_display = ('product', 'author', 'text', 'created_at', 'modified_at')


admin.site.register(Product, ProductAdmin)
admin.site.register(Comment, CommentAdmin)
