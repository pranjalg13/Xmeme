from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import CreateMeme
from django.core import serializers
from .forms import MemeForm,UpdateMemeForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CreateMemeSerializer, UpdateMemeSerializer
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework import viewsets
from django.shortcuts import get_object_or_404, redirect
import coreapi
from rest_framework.schemas import AutoSchema
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import response, schemas


# Schema for Updating meme on swagger
class MemeUpdateSchema(AutoSchema):

    def get_manual_fields(self,path,method):
        extra_fields = []
        if method.lower() in ['patch']:
            extra_fields = [
                coreapi.Field('caption'),
                coreapi.Field('url')
            ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields 

#Schema for Posting meme on Swagger
class MemePostSchema(AutoSchema):
    def get_manual_fields(self,path,method):
        extra_fields = []
        if method.lower() in ['post']:
            extra_fields = [
                coreapi.Field('name', required=True,
                    description='Owner Name'),                
                coreapi.Field('caption',required=True,
                    description='Caption of the Meme'),
                coreapi.Field('url', required=True,
                    description='The Url of meme-image')
            ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields 

# Home Page View
def home(request):
    form = MemeForm()
    allmemes = CreateMeme.objects.all().order_by('-id')
    context = {'form':form, 'allmemes':allmemes}
    return render(request, 'memes/index.html',context)


# Class based APIView for GET and POST request
class MemeSingleViewSet(APIView):
    schema = MemePostSchema()
    def get(self,request):
        memes = CreateMeme.objects.all().order_by('id')[:100]
        serializer = CreateMemeSerializer(memes, many=True)    
        return Response(serializer.data)


    def post(self,request):
        serializer = CreateMemeSerializer(data=request.data)
        try:
            name = request.data['name']
            caption = request.data['caption']
            url = request.data['url']
        except:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        num_results = CreateMeme.objects.filter(name=name).count()
        caption_res = CreateMeme.objects.filter(caption=caption).count()
        url_ct = CreateMeme.objects.filter(url = url).count()
        if(num_results>=1 and caption_res>=1 and url_ct>=1):
            return Response(status=status.HTTP_409_CONFLICT)
        elif serializer.is_valid():
            serializer.save()
            id_meme = serializer.data['id']
            return_id = {'id':str(id_meme)}
            return JsonResponse(return_id)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Class Based APIView For a Single meme for PATCH and GET request.
class MemeViewSet(APIView):

    schema = MemeUpdateSchema()

    def get(self, request, pk):
        try:
            meme = CreateMeme.objects.get(id=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CreateMemeSerializer(meme, many=False)
        return Response(serializer.data)

    
    def patch(self,request,pk):
        try:
            meme = CreateMeme.objects.get(id=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        original_name = meme.name
        data = request.data
        if 'name' in data:
            if(original_name != request.data['name']):
                return Response('Forbidden',status=status.HTTP_403_FORBIDDEN)
        
        serializers = UpdateMemeSerializer(meme, data=data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_405_METHOD_NOT_ALLOWED)


