from django.urls import path
from . import views
from .views import flag_status_api , employees ,employee_detail

urlpatterns = [
    #path('', views.index, name='index'),
    #path('my_view/', views.my_view, name='my_view'),
    path('flag-status/', flag_status_api, name='flag_status_api'),
    path('employees/', employees, name='employees'),
    path('employees/<int:pk>/', employee_detail, name='employee_detail'),
]
