from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name='entry'),
    path('encyclopedia/search', views.search, name='search'),
    path('encyclopedia/create', views.create, name='create')
]
