from django.urls import path
from .views import predict_manual,predict_csv


urlpatterns = [
    path('predict_manual/', predict_manual),
    path('predict_csv/', predict_csv, name='predict_csv'),
   
   ]
