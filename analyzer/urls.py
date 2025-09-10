from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('history/', views.history, name='history'),
    path('download/json/', views.download_json, name='download_json'),
    path('download/csv/', views.download_csv, name='download_csv'),
    path('results/', views.result, name='result'),
]
