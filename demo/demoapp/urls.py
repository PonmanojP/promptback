# myapp/urls.py
from django.urls import path
from .views import  get_chart_data

urlpatterns = [
    path('chart-data/', get_chart_data, name='chart-data'),
]
