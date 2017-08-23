from django.conf.urls import url
from . import views

urlpatterns = [
                url(r'^$', views.index, name='index'),
                url(r'^recipe/new/$', views.recipe_new, name='recipe_new'),
                url(r'^recipe/url/$', views.recipe_from_url, name='recipe_from_url')
                ]
