from django.urls import path
from . import views


urlpatterns =[
    path('', views.index, name="index"),
    path('update_service/<str:pk>/', views.update_service, name='update_service'),
    path('delete_service/<str:pk>/', views.delete_service, name='delete_service')

]