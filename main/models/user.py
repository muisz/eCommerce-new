from django.db import models

seller_ktp_path = "ktp/%Y/%m/"
merchant_image_path = "merchant/"

class Customers(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    birth_date = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    is_seller = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add=True)
    time_created = models.TimeField(auto_now_add=True)

    class Meta:
        db_table = "customers"

class CustomerAddress(models.Model):
    customer_id = models.IntegerField(null=True)
    default = models.BooleanField(default=False)
    provinsi = models.CharField(max_length=100)
    kabupaten = models.CharField(max_length=100)
    kecamatan = models.CharField(max_length=100)
    postcode = models.CharField(max_length=100)
    alamat = models.TextField(null=True)
    
    class Meta:
        db_table = "customers_address"

class Sellers(models.Model):
    customer_id = models.IntegerField()
    nik = models.CharField(max_length=50, unique=True)
    ktp_image = models.ImageField(upload_to=seller_ktp_path)
    
    class Meta:
        db_table = "sellers"

class Merchants(models.Model):
    customer_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=merchant_image_path, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    address = models.TextField()
    date_created = models.DateField(auto_now_add=True)
    time_created = models.TimeField(auto_now_add=True)
    
    class Meta:
        db_table = "merchants"

