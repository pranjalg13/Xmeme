from django.contrib import admin
from django.urls import path,include
from . import views
from .views import MemeViewSet, MemeSingleViewSet
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_swagger.views import get_swagger_view



urlpatterns = [
    path('', views.home,name="home-page"),
    path('memes',MemeSingleViewSet.as_view(), name='meme-list'),
    path('memes/', MemeSingleViewSet.as_view(), name="meme-list-json"),   
    path('memes/<int:pk>',MemeViewSet.as_view(), name='meme-detail'),
]
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])