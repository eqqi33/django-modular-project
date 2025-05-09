from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    barcode = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    class Meta:
        permissions = [
            ("search_product", "Can search Product"),
            ("export_product", "Can export Product"),
        ]