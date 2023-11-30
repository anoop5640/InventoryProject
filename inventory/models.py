from django.db import models

class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    quantity = models.IntegerField()
    reorder_level = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    image = models.ImageField(upload_to='inventory_images/', blank=True, null=True)
    # The 'upload_to' argument specifies a subdirectory for this model's files

    def is_low_stock(self):
        return self.quantity <= self.reorder_level

    def __str__(self):
        return self.name


# Create your models here.
