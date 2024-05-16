from django.db import models

class FeatureFlag(models.Model):
    name = models.CharField(max_length=100)
    is_enabled = models.BooleanField(default=False)

class Employee(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    department = models.CharField(max_length=100)


