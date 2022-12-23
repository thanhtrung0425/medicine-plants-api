from rest_framework import serializers
from .models import MedicinePlants

class MedicinePlantSerializers(serializers.ModelSerializer):
    class Meta:
        model = MedicinePlants
        fields = ('id', 'title', 'preview','description')