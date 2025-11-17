
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('model/', views.model_view, name='model'),
    path('process-model/', views.process_model, name='process_model'),
    path('response/', views.response_view, name='response'),  
]