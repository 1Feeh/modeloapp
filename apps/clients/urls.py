from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('listar/', views.list_clients, name='list_clients'),
    path('adicionar/', views.add_client, name='add_client'),
    path('editar/<int:id_client>/', views.edit_client, name='edit_client'),
    path('excluir/<int:id_client>/', views.delete_client, name='delete_client'),
    path('buscar/', views.search_clients, name='search_clients'),
]