from django.contrib import admin
from app.views import offline_view
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.dashboard, name="Dashboard"),
    path('dress/' ,include('dress.urls'), name="Dress Manager"),
    path('detonador/', include('detonador.urls'), name="Detonador Manager"),
    path('login/', views.login, name="Sign-in Page"),
    path('api/authenticate/', views.authenticateDevice, name="Authenticate IoT Device"),
    path('remote/', include('remote.urls'), name="IR Remote Manager"),
    path('offline/', offline_view, name='offline'),
]
