import json
import csv
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
import redis
from rest_framework import permissions
from .models import MedicinePlants
from .serializers import MedicinePlantSerializers
from django.core.cache import cache

redis_instance = redis.StrictRedis(host='localhost', port=6379, db=0)

class GetAllMedicinePlants(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, *args, **kwargs):
        searchItem = request.GET.get('searchItem')
        if searchItem == None:
            items = MedicinePlants.objects.all()
        else:
            items = MedicinePlants.objects.filter(name__contains=searchItem)
        serializers = MedicinePlantSerializers(items, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    
class UploadDataFromCSV(APIView):
    def get(self, request, *args, **kwargs):
        try:
            with open('/home/thanhtrung/Desktop/DOAN/PBL6/testapi/testapi/myapi/data.csv', 'r') as fileCSV:
                reader = csv.reader(fileCSV)
                items = list(reader)
                originData = MedicinePlants.objects.all()
                for item in items[1:]:
                    if MedicinePlants.objects.filter(id= item[0]).exists:
                        continue
                    else :
                        MedicinePlants.objects.create(
                            id=item[0],
                            title=item[1],
                            preview = item[2],
                            description=item[3])
            return Response({'success': True, 'message': "upload successful"})
        except Exception as e:
            return Response({'error': e.message})
    
class LoadData(viewsets.ViewSet):
    #load to redis
    def loadData(self, request, *args, **kwargs):
        data = cache.get('medicine_plants')
        if data is not None:
            return Response(data)
        else:
            try:
                items = MedicinePlants.objects.all()
                serializers = MedicinePlantSerializers(items, many=True)
                cache.set('medicine_plants', serializers.data, 86400)
                return Response(serializers.data)
            except Exception as e:
                return Response({'success': False, 'message': e.__class__})


class GetItemMedicinePlants(APIView):
    #search using redis
    def get(self, request, *args, **kwargs):
        item_id = request.GET.get('id')
        data = cache.get(item_id)
        if data is not None:
            serializers = MedicinePlantSerializers(data)
            return Response(serializers.data)
        else:
            items = MedicinePlants.objects.filter(name__contains=item_id)
            serializers = MedicinePlantSerializers(items)
            return Response(serializers.data)
        
class ClearCache(APIView):
    def get(self, request, *args, **kwargs):
        result = redis_instance.delete('medicine_plants')
        data = {
            "success" : True,
            "data": result
        }
        return Response(data=data)