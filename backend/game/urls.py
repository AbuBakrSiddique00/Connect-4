from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_root, name='api_root'),
    path('new-game/', views.new_game, name='new_game'),
    path('apply-move/', views.apply_move, name='apply_move'),
    path('ai-move/', views.ai_move, name='ai_move'),
]
