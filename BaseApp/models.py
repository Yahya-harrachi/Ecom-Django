from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    brand = models.CharField(max_length=200, null=True, blank=True)
    category = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    rating = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    numReviews = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    countInStock = models.IntegerField(null=True, blank=True, default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    materiau_principal = models.CharField(max_length=200, null=True, blank=True)
    dimensions = models.CharField(max_length=200, null=True, blank=True)  
    poids = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True) 
    garantie = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class Users(models.Model):
    email = models.EmailField(max_length=191, unique=True)
    username = models.CharField(max_length=100, unique=True)  
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username