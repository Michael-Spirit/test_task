from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from='name', unique=True)
    description = models.TextField(max_length=300)
    price = models.PositiveIntegerField()
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return "/products/%s/" % self.slug

    @property
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.name


class Comment(models.Model):
    product = models.ForeignKey(Product, related_name='comments')
    author = models.CharField(max_length=30, default='Anonymous')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return "/products/%s/" % self.product.slug

    def __str__(self):
        return self.product.name
