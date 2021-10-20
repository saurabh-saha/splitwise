from django.urls import path

from . import views

urlpatterns = [
    path('register', views.register),
    path('expense/<int:user_id>', views.expense),
    path('friends/<int:user_id>', views.friends),
    path('logs/<int:user_id>', views.logs)
]