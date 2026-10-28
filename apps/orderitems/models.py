from django.db import models
from products.models import Product
from orders.models import Order

# Create your models here.
class Orderitem(models.Model):
    quantity = models.IntegerField('Quantidade',null=True, blank=True,default=0)
    unit_price = models.FloatField('Preco unitario',null=True, blank=True, default=0.0)
    subtotal = models.FloatField('Subtotal',null=True, blank=True, default=0.0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')

    class Meta:
        verbose_name = 'Item de pedido'
        verbose_name_plural = 'Itens de pedido'
        ordering =['id']

    def __str__(self):
        return f'{self.id}' 