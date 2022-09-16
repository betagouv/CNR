from django.urls import path
from . import views


urlpatterns = [
    path('', views.index_view, name='index'),
    path('inscription/', views.inscription_view, name='inscription'),
]
