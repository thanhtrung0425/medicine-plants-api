from django.db import models

class MedicinePlants(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id', null=False)
    title = models.CharField(max_length=255, db_column='title', null=True)
    sub_title = models.CharField(max_length=255, db_column='sub_title', null=True)
    science_name = models.CharField(max_length=255, db_column='science_name', null=True)
    plant_family = models.CharField(max_length=255, db_column='plant_family', null=True)
    plant_function = models.TextField(db_column='plant_function', null=True)
    dosage_usage = models.TextField(db_column='dosage_usage', null=True)
    image_url = models.CharField(max_length=255, db_column='image_url', null=True)
    
    class Meta:
        db_table='MedicinePlants'