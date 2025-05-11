from rest_framework import serializers

from .models import CatDogPrediction


class CatDogPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatDogPrediction
        fields = "__all__"
