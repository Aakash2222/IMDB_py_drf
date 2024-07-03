from django.shortcuts import render, HttpResponse
from .models import WatchList, StreamPlatform, Review
from .serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from django.http import JsonResponse
from django.http import Http404
from rest_framework.exceptions import ValidationError
from .permissions import AdminOrReadOnly
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser , IsAuthenticatedOrReadOnly
from .permissions import AdminOrReadOnly, ReviewUserOrReadOnly
# Create your views here.

# entry point -we should give enrty point to list things
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'watchlist': reverse('watchlist-list', request=request, format=format),
        'streamplatform': reverse('streamplatform-list', request=request, format=format)
    })


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        movie = WatchList.objects.get(pk=pk) 
        review_user=self.request.user #taking user detail who is doing review

        # checking if the user has already reviewed this movie       
        review_queryset= Review.objects.filter(review_user=review_user, watchlist=movie)
        print(review_queryset)
        if review_queryset.exists():
            raise ValidationError("Already Review done!!!")
        if movie.number_rating == 0:
            movie.av_rating = serializer.validated_data['rating']
        else:
            movie.av_rating = (movie.av_rating * movie.number_rating + serializer.validated_data['rating'] ) / (movie.number_rating +1)

        movie.number_rating += 1   
        movie.save() 
        serializer.save(watchlist = movie, review_user=review_user)
 
    def get_queryset(self):
        return Review.objects.all()
    

# class ReviewListView(generics.ListCreateAPIView):  commenting bcoz we want only readonly mode
class ReviewListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    # overrideing  - https://www.django-rest-framework.org/api-guide/filtering/
    # get_queryset
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist = pk)



# review of particular movie
class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [ReviewUserOrReadOnly]  #only user who did review can modify
    # permission_classes = [AdminOrReadOnly]  #only admin can modify
    queryset = Review.objects.all() 
    serializer_class = ReviewSerializer


class StreamPlatformViewSet(viewsets.ModelViewSet):
    
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer


class WatchListViewSet(viewsets.ModelViewSet):
    
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer


