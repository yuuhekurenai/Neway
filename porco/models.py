from django.db import models


class Product(models.Model):
    COLOR_CHOICES = [
        ('red', 'Vermelho'),
        ('blue', 'Azul'),
        ('green', 'Verde'),
        ('yellow', 'Amarelo'),
        # Adicione outras opções de cores conforme necessário.
    ]

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='white')


