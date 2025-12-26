from django.urls import path
from . import views

urlpatterns = [
    # Telas do Usuário
    path('', views.index, name="ir_dashboard"),
    path('control/<int:pk>/', views.remote_interface, name="ir_interface"),
    
    # Comandos AJAX (Browser -> Django)
    path('api/click/<int:btn_id>/', views.trigger_signal, name="ir_click"),
    path('api/learn/<int:remote_id>/', views.start_learning, name="ir_learn_mode"),

    path('api/callback/save/', views.save_learned_button, name="ir_save_callback"),
]