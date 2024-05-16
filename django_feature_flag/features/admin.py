from django.contrib import admin
from .models import FeatureFlag , Employee

# Register your models here.
admin.site.register(FeatureFlag)
admin.site.register(Employee)