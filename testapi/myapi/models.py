from django.db import models

class MedicinePlants(models.Model):
    id = models.AutoField(primary_key=True, db_column='id', null=False)
    title = models.CharField(max_length=255, db_column='title', null=True)
    preview = models.CharField(max_length=255, db_column='preview', null=True)
    description = models.CharField(max_length=65535, db_column='description', null=True)
