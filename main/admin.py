from django.contrib import admin
from .models.user import Customers, CustomerAddress, Sellers, Merchants
from .models.product import Products, ProductSpecifications, ProductMedia, ProductVarians, ProductTags, Categories, Orders, AdditionalFees, SubtractionFees, Promo, Vouchers, References

admin.site.register(Customers)
admin.site.register(CustomerAddress)
admin.site.register(Sellers)
admin.site.register(Merchants)
admin.site.register(Products)
admin.site.register(ProductSpecifications)
admin.site.register(ProductMedia)
admin.site.register(ProductVarians)
admin.site.register(ProductTags)
admin.site.register(Categories)
admin.site.register(Orders)
admin.site.register(AdditionalFees)
admin.site.register(SubtractionFees)
admin.site.register(Promo)
admin.site.register(Vouchers)
admin.site.register(References)