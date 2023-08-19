from django.db import models

class VisitCountModel(models.Model):
    count = models.IntegerField(default=0)