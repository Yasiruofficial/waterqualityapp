from django.urls import path
from . import views

urlpatterns = [
    path('', views.testapi,name="testapi"),
]
