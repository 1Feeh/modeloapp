from django.urls import path
from . import views

app_name = 'invoices'

urlpatterns = [
    path('<int:invoice_id>/', views.view_invoice, name='view_invoice'),
]