from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('', ServicesList.as_view(), name="services"),
    path('services/<int:pk>/', ServicesDetail.as_view(), name="service"),
    path('service-update/<int:pk>/', ServicesUpdate.as_view(), name="service-update"),
    path('service-delete/<int:pk>/', ServicesDelete.as_view(), name="service-delete"),
    path('create-service/', ServicesCreate.as_view(), name="create-service"),
    path('type-of-work/', TypeOfWorkList.as_view(), name="typeofwork"),
    path('work_create/', TypeOfWorkCreate.as_view(), name="work_create"),
    path('work_detail/<int:pk>/', TypeOfWorkDetail.as_view(), name="work_detail"),
    path('work-update/<int:pk>/', TypeOfWorkUpdate.as_view(), name="work_update"),
    path('work-delete/<int:pk>/', TypeOfWorkDelete.as_view(), name="work_delete"),
]