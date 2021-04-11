from rest_framework import serializers
from .models.user import Customers, CustomerAddress, Sellers

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