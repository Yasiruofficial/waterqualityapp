from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict_im,name="ml_predict_im"),
    path('reg/', views.reg_im,name="ml_reg_im"),
    path('current/', views.current_data_im,name="ml_reg_im"),
]
