from rest_framework import serializers
from .models import Photo

class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Photo
        fields = (
            'width',
        )

    def create(self, validated_data):
        return Photo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.width = validated_data.get('width', instance.width)
        return instance