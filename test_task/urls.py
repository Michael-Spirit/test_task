from django.conf.urls import url
from django.contrib import admin
from product import views
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='index')),
    url(r'^admin/', admin.site.urls),
    url(r'^login/', auth_views.login, name='login'),
    url(r'^register/', views.register, name='register'),
    url(r'^logout/', auth_views.logout, name='logout'),
    url(r'^products/$', views.index, name='index'),
    url(r'^products/(?P<product_slug>[a-z0-9]+(?:-[a-z0-9]+)*)/$',
        views.get, name='product'),
    url(r'^like/(?P<product_slug>[a-z0-9]+(?:-[a-z0-9]+)*)/$',
        views.like, name='like')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
