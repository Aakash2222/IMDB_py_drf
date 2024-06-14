from django.shortcuts import render, HttpResponse
from .models import WatchList, StreamPlatform
from .serializers import WatchListSerializer, StreamPlatformSerializer
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.

def movie_list(request):

    movie_list = WatchList.objects.all()
    serialized = WatchListSerializer(movie_list, many=True)
    return JsonResponse(serialized.data, safe=False)

def movie_detail(request, pk):

    movie = WatchList.objects.get(pk=pk)
    serialized = WatchListSerializer(movie)
    return JsonResponse(serialized.data)


@api_view(['GET', 'POST'])
def stream_list(request):
    # list all code streamplatform, or create a new streamplatform.
    if request.method == 'GET':
        stream_list = StreamPlatform.objects.all()
        serialized = StreamPlatformSerializer(stream_list,many=True)
        return Response(serialized.data)
    
    elif request.method == 'POST':
        _data = request.data
        serialized = StreamPlatformSerializer(data=_data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data,status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST )


@api_view(['GET', 'PUT', 'DELETE'])
def stream_detail(request, pk):
    # retrive,update,or delete.
    try:
        stream_platform = StreamPlatform.objects.get(pk=pk)
    except StreamPlatform.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serialized = StreamPlatformSerializer(stream_platform)
        return Response(serialized.data)
    
    elif request.method == 'PUT':
        _data = request.data
        serialized = StreamPlatformSerializer(stream_platform, data=_data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        StreamPlatform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)