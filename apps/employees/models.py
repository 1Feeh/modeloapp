from django.db import models
from persons.models import Person

# Create your models here.
class Employee(Person):
    salary = models.FloatField('Preco unitario',null=True, blank=True, default=0.0)
    position = models.CharField('Nome', max_length=100)

    class Meta:
        verbose_name = 'Funcionario'
        verbose_name_plural = 'Funcionarios'
        ordering =['id']

    def __str__(self):
        return super().first_name
        # ou pode ser usado "return super().__str__()"