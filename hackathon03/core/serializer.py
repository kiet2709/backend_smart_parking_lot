from rest_framework import serializers
from core.models import Camera
from core.models import ObjectResponse


class CameraSerializer(serializers.ModelSerializer):

    class Meta:
        model = Camera
        fields = "__all__"

class ObjectResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = ObjectResponse
        fields = "__all__"


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20, required=True)
    password = serializers.CharField(max_length=128, write_only=True)

    def create(self, validated_data):
        return validated_data