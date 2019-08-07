from rest_framework import serializers
from .models import Photo
from django.contrib.auth.models import User

class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
        )

    def create(self, validated_data):
        return User.objects.create(**validated_data)
