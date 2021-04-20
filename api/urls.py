from django.urls import path
from . import views

urlpatterns = [
    path('', views.ml_predict_mobile,name="ml_predict_mobile"),
]
