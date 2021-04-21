from django.contrib import admin
from .models.user import Customers, CustomerAddress, Sellers, Merchants
from .models.product import Products, ProductSpecifications, ProductTags, Categories, Orders, Promo, Vouchers, References
from .models.pengiriman import Pengiriman

admin.site.register(Customers)
admin.site.register(CustomerAddress)
admin.site.register(Sellers)
admin.site.register(Merchants)
admin.site.register(Products)
admin.site.register(ProductSpecifications)
admin.site.register(ProductTags)
admin.site.register(Categories)
admin.site.register(Orders)
admin.site.register(Promo)
admin.site.register(Vouchers)
admin.site.register(References)
admin.site.register(Pengiriman)