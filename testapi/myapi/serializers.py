from rest_framework import serializers
from .models import MedicinePlants

class MedicinePlantSerializers(serializers.ModelSerializer):
    class Meta:
        model = MedicinePlants
        fields = ["id", "title", "sub_title", "science_name", "plant_family", "plant_function", "dosage_usage", "image_url"]