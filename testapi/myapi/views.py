import json
import csv
import redis

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from .models import MedicinePlants
from .serializers import MedicinePlantSerializers
from django.core.cache import cache

redis_instance = redis.StrictRedis(host='localhost', port=6379, db=0)

class UploadDataFromCSV(APIView):
    def get(self, request, *args, **kwargs):
        cur_db = MedicinePlants.objects.all()
        if cur_db.count() == 0:
            try:
                with open('/home/thanhtrung0425/app-api/medicine-plants-api/testapi/myapi/data.csv', 'r') as fileCSV:
                    reader = csv.reader(fileCSV)
                    items = list(reader)
                    
                    for item in items[1:]:
                        if MedicinePlants.objects.filter(id=item[0]).exists():
                            continue
                        else :
                            MedicinePlants.objects.create(
                                id=item[0],
                                title=item[1],
                                sub_title=item[2],
                                science_name=item[3],
                                plant_family = item[4],
                                plant_function=item[5],
                                dosage_usage=item[6],
                                image_url=item[7])
 
                return Response({"Status: ": status.HTTP_200_OK, "message": "Database uploaded"})
            except Exception as e:
                return Response({'error': e})
        else:
            return Response({"Status: ": status.HTTP_200_OK, "message": "Database exists"})

class LoadData(viewsets.ViewSet):
    #load to redis
    def loadData(self, request, *args, **kwargs):
        data = redis_instance.get('medicine_plants')
        cur_db = MedicinePlants.objects.all()
        
        if data is not None:
            return Response(json.loads(data))
        elif cur_db.count() != 0:
            try:
                serializers = MedicinePlantSerializers(cur_db, many=True)
                
                #setup data to cache
                json_data = json.dumps(serializers.data)
                redis_instance.set('medicine_plants', json_data)
                
                for item in serializers.data:
                    cache.set(item['id'], json.dumps(item))

                return Response(serializers.data)
            except Exception as e:
                return Response({'Success': False, 'message': e.__class__})
        else:
            UploadDataFromCSV.get(self, request)
            return Response({"Status: ": status.HTTP_200_OK, "message": "Database uploaded"})

class GetItemMedicinePlants(APIView):
    #search using redis
    def get(self, request, *args, **kwargs):
        item_id = self.kwargs['id']
        
        data = cache.get(item_id)
        if data is not None:
            return Response(json.loads(data))
        else:
            try:
                item = MedicinePlants.objects.get(id = item_id)
                if item is None:
                    LoadData.loadData(self, request)
                    item = MedicinePlants.objects.get(id = item_id)

                serializer = MedicinePlantSerializers(item)
                cache.set(item_id, json.dumps(serializer.data))
                return Response(serializer.data)
            except Exception as e:
                return Response({'status': status.HTTP_404_NOT_FOUND})

class ClearCache(APIView):
    def get(self, request, *args, **kwargs):
        result = redis_instance.delete('medicine_plants')
        data = {
            "success" : True,
            "data": result
        }
        return Response(data=data)