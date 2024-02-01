from django.db import models
from PIL import Image
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    class Meta:
        app_label = 'prod'
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.PositiveIntegerField(default=0)
    is_loan = models.BooleanField(default=False)

    
    def __str__(self):
        return self.name


class Staff(models.Model):
    SHOP = 'Shop'
    STORE = 'Store'

    LOCATION_CHOICES = [
        (SHOP, 'Shop'),
        (STORE, 'Store'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    salary = models.PositiveIntegerField(default=0)
    position = models.CharField(
        max_length=5,
        choices=LOCATION_CHOICES,
        default=SHOP,
    )
    phone_num = models.CharField(max_length=10, null=True)
    national_id = models.CharField(max_length=10, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='staff_profile_pics/', blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

from django.db import models
from django.core.exceptions import ValidationError
from .models import Product, Staff
class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    quantity_sold = models.PositiveIntegerField()
    sale_date = models.DateField(default=timezone.now)
    sold_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    is_loan = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        # Validate the quantity sold
        if self.quantity_sold > self.product.quantity_available:
            raise ValidationError("Quantity sold cannot exceed available quantity.")

        # Calculate and set the sold_amount before saving
        
        # Decrement the available quantity of the product
        self.product.quantity_available -= self.quantity_sold
        self.product.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Sale ID: {self.id}, Product: {self.product.name}, Quantity Sold: {self.quantity_sold}, Sale Date: {self.sale_date}, Is Loan: {self.is_loan}"

from django.db.models.signals import post_save
from django.dispatch import receiver

class Credit(models.Model):
    sale = models.OneToOneField(Sale, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Credit ID: {self.id}, Sale ID: {self.sale.id}, Amount: {self.amount}"

    @receiver(post_save, sender=Sale)
    def create_credit(sender, instance, created, **kwargs):
        if created and instance.is_loan:
            Credit.objects.create(sale=instance, amount=instance.sold_amount)





# models.py


from django.utils import timezone
class Attendance(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)

    def mark_check_in(self):
        self.check_in_time = timezone.now()
        self.save()

    def mark_check_out(self):
        self.check_out_time = timezone.now()
        self.save()

    def is_absent(self):
        return self.check_in_time is None or self.check_out_time is None
# models.py


