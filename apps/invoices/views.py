from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from invoices.models import Invoice
from django.contrib.auth.decorators import login_required

# Create your views here.
#@login_required(login_url='/contas/login/')
def create_invoice_for_order(order):
    if hasattr(order, 'invoice'):
        return order.invoice
    invoice_number = f'NF-{order.id:06d}'
    return Invoice.objects.create(
        order=order,
        number=invoice_number
    )

def view_invoice(request, invoice_id):
    template_name = 'invoices/view_invoice.html'
    invoice = get_object_or_404(Invoice, id=invoice_id)
    context = {
        'invoice': invoice,
        'order': invoice.order,
        'items': invoice.order.items.all()
    }
    return render(request, template_name, context)