
from django.contrib import admin
from django.urls import path,include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('list/',views.movie_list, name='movie-list'),
    path('list/<int:pk>', views.movie_detail, name='movie-detail'),
    
    # path('stream/', views.stream_list, name = 'stream-platform'),
    path('stream/', views.StreamPlatformList.as_view(), name = 'stream-platform'),
    
    # path('stream/<int:pk>', views.stream_detail, name = 'stream-detail'),
    path('stream/<int:pk>', views.StreamPlatformDetail.as_view(), name = 'stream-detail'),
]


urlpatterns = format_suffix_patterns(urlpatterns)
