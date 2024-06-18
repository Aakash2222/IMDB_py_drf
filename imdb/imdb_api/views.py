from django.shortcuts import render, HttpResponse
from .models import WatchList, StreamPlatform
from .serializers import WatchListSerializer, StreamPlatformSerializer
from django.http import JsonResponse
from django.http import Http404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.reverse import reverse
# Create your views here.

# entry point
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        # 'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


def movie_list(request):

    movie_list = WatchList.objects.all()
    serialized = WatchListSerializer(movie_list, many=True)
    print(serialized)
    return JsonResponse(serialized.data, safe=False)

def movie_detail(request, pk):

    movie = WatchList.objects.get(pk=pk)
    serialized = WatchListSerializer(movie)
    return JsonResponse(serialized.data) 


# @api_view(['GET', 'POST'])
# def stream_list(request):
#     # list all code streamplatform, or create a new streamplatform.
#     if request.method == 'GET':
#         stream_list = StreamPlatform.objects.all()
#         serialized = StreamPlatformSerializer(stream_list,many=True)
#         return Response(serialized.data)
    
#     elif request.method == 'POST':
#         _data = request.data
#         serialized = StreamPlatformSerializer(data=_data)
#         if serialized.is_valid():
#             serialized.save()
#             return Response(serialized.data,status=status.HTTP_201_CREATED)
#         return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST )

# @api_view(['GET', 'PUT', 'DELETE'])
# def stream_detail(request, pk):
#     # retrive,update,or delete.
#     try:
#         stream_platform = StreamPlatform.objects.get(pk=pk)
#     except StreamPlatform.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == 'GET':
#         serialized = StreamPlatformSerializer(stream_platform)
#         return Response(serialized.data)
    
#     elif request.method == 'PUT':
#         _data = request.data
#         serialized = StreamPlatformSerializer(stream_platform, data=_data)
#         if serialized.is_valid():
#             serialized.save()
#             return Response(serialized.data)
#         return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     elif request.method == 'DELETE':
        # StreamPlatform.delete()
        # return Response(status=status.HTTP_204_NO_CONTENT)




# class-based-view using APIView:
# class StreamPlatformList(APIView):
#     """
#     List all snippets, or create a new snippet.
#     """

#     def get(self, request, format=None):
#         stream_list = StreamPlatform.objects.all()
#         serialized = StreamPlatformSerializer(stream_list,many=True)
#         return Response(serialized.data)
    
#     def post(self, request, format=None):
#         _data = request.data
#         serialized = StreamPlatformSerializer(data=_data)
#         if serialized.is_valid():
#             serialized.save()
#             return Response(serialized.data,status=status.HTTP_201_CREATED)
#         return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST )


# class StreamPlatformDetail(APIView):
#     def get_object(self,pk):
#         try:
#             return StreamPlatform.objects.get(pk=pk)
#         except StreamPlatform.DoesNotExist:
#             raise Http404
        
#     def get(self, request,pk, format=None):
#         stream_platform = self.get_object(pk)
#         serialized = StreamPlatformSerializer(stream_platform)
#         return Response(serialized.data)
        
#     def put(self, request,pk, format=None):
#         stream_platform = self.get_object(pk)
#         _data = request.data
#         serialized = StreamPlatformSerializer(stream_platform, data=_data)
#         if serialized.is_valid(): 
#             serialized.save()
#             return Response(serialized.data)
#         return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
#     def delete(self,request,pk,format=None):
#         stream_platform = self.get_object(pk)
#         StreamPlatform.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class-based-view -Using mixins
# class StreamPlatformList(mixins.ListModelMixin,
#                          mixins.CreateModelMixin,
#                          generics.GenericAPIView):
    
    
#     queryset = StreamPlatform.objects.all()
#     serializer_class = StreamPlatformSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# class StreamPlatformDetail(mixins.RetrieveModelMixin,
#                 mixins.UpdateModelMixin,
#                 mixins.DestroyModelMixin,
#                 generics.GenericAPIView):
        
#     queryset = StreamPlatform.objects.all()
#     serializer_class = StreamPlatformSerializer 

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)



# Using generic class-based views
class StreamPlatformList(generics.ListCreateAPIView):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer


class StreamPlatformDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer