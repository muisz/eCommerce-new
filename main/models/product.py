from django.db import models
import uuid

product_media_path = "product/%Y/%m/"
supplier_choices = (
    ('app', 'app'), # app which mean this or our company that own this service
    ('merchant', 'merchant')
)
payment_status = (
    ('checkout', 'checkout'),
    ('fail', 'fail'),
    ('success', 'success'),
)

class Products(models.Model):
    merchant_id = models.IntegerField()
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    stocks = models.IntegerField(default=1)
    category_id = models.IntegerField()
    varian = models.TextField(null=True, default='[]')
    media = models.TextField(null=True, default='[]')
    date_created = models.DateField(auto_now_add=True)
    time_created = models.TimeField(auto_now_add=True)

    class Meta:
        db_table = "products"

class ProductSpecifications(models.Model):
    product_id = models.IntegerField()
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    
    class Meta:
        db_table = "product_specifications"

class ProductTags(models.Model):
    product_id = models.IntegerField()
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = "product_tags"

class Categories(models.Model):
    merchant_id = models.IntegerField()
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = "product_categories"

class Orders(models.Model):
    product_id = models.IntegerField()
    customer_id  = models.IntegerField()
    pre_total = models.FloatField()
    total = models.FloatField()
    payment_status = models.CharField(max_length=100, choices=payment_status, default="checkout")
    date_pay = models.DateField(null=True)
    time_pay = models.TimeField(null=True)
    additional_fee = models.TextField(null=True, default='[]')
    payment_data = models.TextField(null=True)
    shipment_data = models.TextField(null=True)
    invoice = models.UUIDField(default=uuid.uuid4)
    order_status = models.CharField(max_length=100, default='menunggu pembayaran', null=True)
    order_status_update = models.DateTimeField(null=True)
    date_created = models.DateField(auto_now_add=True)
    time_created = models.TimeField(auto_now_add=True)
    
    class Meta:
        db_table = "orders"

class Promo(models.Model):
    name = models.CharField(max_length=100)
    value = models.FloatField()
    is_percent = models.BooleanField(default=False)
    supplier = models.CharField(max_length=100, choices=supplier_choices)
    supplier_id = models.IntegerField() # for merchant only
    ref_id = models.IntegerField()
    date_created = models.DateField(auto_now_add=True)
    time_created = models.TimeField(auto_now_add=True)
    
    class Meta:
        db_table = "promo"
    
class Vouchers(models.Model):
    name = models.CharField(max_length=100, unique=True)
    value = models.FloatField()
    is_percent = models.BooleanField(default=False)
    supplier = models.CharField(max_length=100, choices=supplier_choices)
    supplier_id = models.IntegerField() # for merchant only
    ref_id = models.IntegerField()
    date_created = models.DateField(auto_now_add=True)
    time_created = models.TimeField(auto_now_add=True)
    
    class Meta:
        db_table = "vouchers"

class References(models.Model):
    code = models.CharField(max_length=50, unique=True)
    value = models.CharField(max_length=100, unique=True)
    ## value initial
    # merchant_xxx for merchant
    # promo_xxx for promo
    # voucher_xxx for voucher
    # and etc.

    class Meta:
        db_table = "references"