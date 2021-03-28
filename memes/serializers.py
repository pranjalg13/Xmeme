# serializers.py
from rest_framework import serializers

from .models import CreateMeme

# CreateMemeSerializer
class CreateMemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateMeme
        fields = ['id','name', 'url','caption']

# UpdateMeme serializer
class UpdateMemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateMeme
        fields = ['url','caption']