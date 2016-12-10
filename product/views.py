from django.views.decorators.cache import cache_page

try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login
from datetime import timedelta
from django.utils import timezone
from django.contrib import messages
from product.forms import CommentForm, ProductForm, MyUserCreationForm

from .models import Product, Comment


# Create your views here.
def index(request, template='index.html'):
    sorts = ('likes', '-likes')

    page = request.GET.get('page')
    sort = request.GET.get('sort')
    products = Product.objects.all()

    # sort
    if sort in sorts:
        products = products.order_by(sort)

    # paginator
    paginator = Paginator(products, 5)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    # add new product form
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "You have successfully added the product.")
            return redirect('index')
        else:
            messages.error(
                request, "Something went wrong with adding the product.")
            return TemplateResponse(request, template,
                                    {'products': products, 'form': form})

    form = ProductForm()
    return TemplateResponse(request, template,
                            {'products': products, 'form': form})


def get(request, product_slug, template='product/product.html'):
    liked = False

    product = get_object_or_404(Product, slug=product_slug)
    comment_lte = timezone.now() - timedelta(hours=24)
    comments = Comment.objects.filter(
        product=product, created_at__gte=comment_lte).order_by("-created_at")

    if request.user.is_authenticated():
        if product.likes.filter(id=request.user.id).exists():
            liked = True

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            if request.user.is_authenticated():
                comment.author = request.user.username
            comment.product = product
            comment.save()
            messages.success(request, "You commented on the product")
            return redirect(product.get_absolute_url())
        else:
            messages.error(
                request, "Something went wrong with adding a comment.")
            return TemplateResponse(
                request, template, {
                    'form': form,
                    'product': product,
                    'comments': comments,
                    'liked': liked
                })

    form = CommentForm()
    return TemplateResponse(request, template, {
        'form': form,
        'product': product,
        'comments': comments,
        'liked': liked
    })


def register(request, template='registration/register.html'):
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "You have successfully registered.")
            return redirect('index')
        else:
            return TemplateResponse(request, template, {'form': form})

    form = MyUserCreationForm()
    return render(request, template, {'form': form})


@login_required
@require_POST
@cache_page(60 * 15)  # cached for 15 minutes
def like(request, product_slug):
    data = {}
    django_messages = []
    user = request.user
    product = Product.objects.select_related().get(slug=product_slug)

    if not product.likes.filter(id=user.id).exists():
        product.likes.add(user)
        messages.success(request, 'You liked this.')

    # catch messages for ajax
    for message in messages.get_messages(request):
        django_messages.append({
            "message": message.message,
            "tags": message.tags,
        })
    data['messages'] = django_messages

    ctx = {'likes_count': product.total_likes, 'data': data}
    return HttpResponse(json.dumps(ctx), content_type='application/json')
