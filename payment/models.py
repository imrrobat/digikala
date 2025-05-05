from django.db import models
from django.contrib.auth.models import User 
from shop.models import Product
from django.db.models.signals import post_save 
from django_jalali.db import models as jmodels 
import jdatetime
import uuid

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shipping_full_name = models.CharField(max_length=250)
    shipping_email = models.CharField(max_length=250)
    shipping_address1 = models.CharField(max_length=250, blank=True)
    shipping_address2 = models.CharField(max_length=250, blank=True, null=True)
    shipping_city = models.CharField(max_length=25, blank=True)
    shipping_state = models.CharField(max_length=25, blank=True, null=True)
    shipping_zipcode = models.CharField(max_length=25, blank=True, null=True)
    shipping_country = models.CharField(max_length=25, default = 'IRAN')

    class Meta:
        verbose_name_plural = 'Shipping Address'

    def __str__(self):
        return f'Shipping Address - {str(self.shipping_full_name)}'

def create_shipping_user(sender, instance, created, **kwargs):
    if created:
        user_shipping = ShippingAddress(user=instance)
        user_shipping.save()
        
post_save.connect(create_shipping_user, sender=User)

class Order(models.Model):
    STATUS_ORDER = [
        ('Pending', 'در انتظار پرداخت'),
        ('Processing', 'در حال پردازش'),
        ('Shipped', 'ارسال شده به پست'),
        ('Delivered', 'تحویل داده شده'),
        ('Cancelled','سفارش لغو شده'),
        ('Failed','پرداخت ناموفق')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=300)
    shipping_address = models.TextField(max_length=150000)
    amount_paid = models.DecimalField(decimal_places=0 , max_digits=12)
    date_ordered = jmodels.jDateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_ORDER, default='Pending')
    last_update = jmodels.jDateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    def save(self, *args, **kwargs):
        if self.pk:
            old_status = Order.objects.get(id=self.pk).status
            
            if old_status != self.status:
                self.last_update = jdatetime.datetime.now()
        
        super().save(*args, **kwargs)
        
    
    
    def __str__(self):
        return f'Order - {str(self.id)}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    quantity = models.PositiveIntegerField(default = 1)
    price = models.DecimalField(decimal_places=0 , max_digits=12)
    
    def __str__(self):
        if self.user is not None:
            return f'Order Item - {str(self.id)} - for {self.user}'
        else:
            return f'Order Item - {str(self.id)}'