from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="detonador_dashboard"),
    path('evento/activate/<int:evento_id>/', views.activate_event, name='activate_event'),
    path('evento/delete/<int:evento_id>/', views.delete_event, name='delete_event'),
]
