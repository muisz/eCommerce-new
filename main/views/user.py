from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models.user import Customers, CustomerAddress, Sellers, Merchants
from ..serializers import CustomerSerializer, CustomerAddressSerializer, SellerSerializer, MerchantSerializer
from utils.response import AssertionErrorResponse, ErrorResponse, SuccessResponse
from utils.utils import generateHash, checkIsExists
import json

class CustomerView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = CustomerSerializer(data = data)
            if serializer.is_valid():
                saved = serializer.save()
                saved.password = generateHash(data['password'])
                saved.save()

                include_address = False
                address_saved = None

                if 'address' in data and data['address'] != {}:
                    address = data['address']
                    if not isinstance(address, dict):
                        temp = json.dumps(address)
                        address = json.loads(temp)
                    address_serializer = CustomerAddressSerializer(data = address)
                    if address_serializer.is_valid():
                        address_saved = address_serializer.save()
                        address_saved.default = True
                        address_saved.customer_id = saved.id
                        address_saved.save()
                        include_address = True
                resp = {
                    "message":"data successfully added!",
                    "data": CustomerSerializer(saved, many=False).data
                }
                if include_address:
                    resp['address'] = CustomerAddressSerializer(address_saved, many=False).data
                return SuccessResponse(resp)

            else:
                raise

        except AssertionError as error:
            return AssertionErrorResponse(str(error))

        except:
            return ErrorResponse("Bad Request")

class SellersView(APIView):
    def post(self, request):
        try:
            data = request.data
            customer_id = data['customer_id']
            customer = checkIsExists(Customers, id = customer_id)
            assert customer, "customer_id not found::404"
            serializer = SellerSerializer(data = data)
            if serializer.is_valid():
                saved = serializer.save()
                customer.is_seller = True
                customer.save()
                return SuccessResponse({"message":"data successfully added!"})
            else:
                raise

        except AssertionError as error:
            return AssertionErrorResponse(str(error))

        except:
            return ErrorResponse("Bad Request")

class MerchantView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = MerchantSerializer(data = data)
            if serializer.is_valid():
                is_exist = checkIsExists(Sellers, customer_id = data['customer_id'])
                assert is_exist, "customer not found::404"
                saved = serializer.save()
                return SuccessResponse({"data": MerchantSerializer(saved).data})

            else:
                raise AssertionError("invalid data::400")

        except AssertionError as error:
            return AssertionErrorResponse(str(error))

    def get(self, request):
        try:
            data_raw = Merchants.objects.all()
            data = MerchantSerializer(data_raw, many=True).data
            return SuccessResponse({"data": data})

        except AssertionError as error:
            return AssertionErrorResponse(str(error))