from django.urls import path
from . import views

app_name = 'employees'

urlpatterns = [
    path('listar/', views.list_employees, name='list_employees'),
    path('adicionar/', views.add_employee, name='add_employee'),
    path('editar/<int:id_employee>/', views.edit_employee, name='edit_employee'),
    path('excluir/<int:id_employee>/', views.delete_employee, name='delete_employee'),
]