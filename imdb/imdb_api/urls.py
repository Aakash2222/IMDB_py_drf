
from django.contrib import admin
from  django.urls import path,include
from .views import api_root,WatchListViewSet
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'stream', views.StreamPlatformViewSet, basename='streamplatform')
router.register(r'list', views.WatchListViewSet, basename='watchlist')



urlpatterns = [
    # path('list/',watchlist_list, name='watchlist-list'),
    # path('list/<int:pk>', watchlist_detail, name='watchlist-detail'),
    

    path('list/<int:pk>/review/', views.ReviewListView.as_view(), name='review-list'),
    path('list/<int:pk>/review-create/', views.ReviewCreate.as_view(), name='review-create'),
  
    path('list/review/<int:pk>/',views.ReviewDetailView.as_view(), name='review-detail'),
         
    


    path('', include(router.urls)),        
    path('', views.api_root),
]


