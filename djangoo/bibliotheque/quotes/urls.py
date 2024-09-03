from django.urls import path
from . import views

urlpatterns = [
    path('', views.quote_list, name='quote_list'),
    path('add/', views.add_quote, name='add_quote'),
    path('edit/<int:pk>/', views.edit_quote, name='edit_quote'),
    path('delete/<int:pk>/', views.delete_quote, name='delete_quote'),
]
