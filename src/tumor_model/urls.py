from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('model/', views.model_view, name='model'),
    path('process-model/', views.process_model, name='process_model'),
    path('api/simulate/', views.api_simulate, name='api_simulate'),
    path('response/', views.api_simulate, name='response'),
    path('patient-form/', views.patient_form, name='patient_form'), ###----- добавила
]