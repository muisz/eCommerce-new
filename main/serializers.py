from rest_framework import serializers
from .models.user import Customers, CustomerAddress, Sellers, Merchants, Carts
from .models.product import Categories, Products

# user

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = '__all__'
        extra_kwargs = {'password': { "write_only": True }}
        
class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        fields = '__all__'

class SellerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Sellers
		fields = '__all__'

class MerchantSerializer(serializers.ModelSerializer):
    address = serializers.JSONField()
    class Meta:
        model = Merchants
        fields = ['id', 'customer_id', 'name', 'image', 'description', 'address', 'date_created', 'time_created']

class CartSerializer(serializers.ModelSerializer):
    varian = serializers.JSONField()
    class Meta:
        model = Carts
        fields = ['id', 'customer_id', 'product_id', 'name', 'quantity', 'varian', 'price', 'date_created']

# product
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id', 'name', 'description', 'price']
