from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models.user import Customers, CustomerAddress, Sellers, Merchants
from ..serializers import CustomerSerializer, CustomerAddressSerializer
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
                return SuccessResponse({"message":"data successfully added!"})

            else:
                raise

        except AssertionError as error:
            return AssertionErrorResponse(str(error))

        except:
            return ErrorResponse("Bad Request")