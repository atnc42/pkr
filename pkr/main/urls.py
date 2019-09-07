
from django.contrib import admin
from django.urls import path
from main import views
app_name = 'main'

urlpatterns = [
    path('', views.SayMyName.as_view(), name='say_my_name'),
]
