from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models.user import Customers, CustomerAddress, Sellers, Merchants, Carts
from ..models.product import Products
from ..serializers import CustomerSerializer, CustomerAddressSerializer, SellerSerializer, MerchantSerializer, CartSerializer
from utils.response import AssertionErrorResponse, ErrorResponse, SuccessResponse
from utils.utils import generateHash, checkIsExists, getPaginate, query
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

class CartView(APIView):
    def saveData(self, data, product):
        ## data request
        ## customer_id: int
        ## product_id: int
        ## quantity: int
        ## varian: json list
        ##   - context: string
        ##   - name: string
        ##   - is_price: boolean
        ##   - price: optional float
        try:
            saved = Carts.objects.create(
                customer_id = data['customer_id'],
                product_id = data['product_id'],
                name = product.name,
                quantity = data['quantity'],
                varian = json.dumps(data['varian']),
                price = product.price
            )
            return saved

        except:
            return False

    def checkVarianExist(self, data_request, varian_exist):
        varian_exist_length = len(varian_exist)
        same_data_length = 0
        for data in data_request:
            for varian in varian_exist:
                if data['context'] == varian['context'] and data['name'] == varian['name']:
                    same_data_length += 1
        return same_data_length == varian_exist_length

    def post(self, request):
        try:
            data = request.data
            customer = checkIsExists(Customers, id = data['customer_id'])
            product = checkIsExists(Products, id = data['product_id'])

            assert customer, "customer not found::404"
            assert product, "product not found::404"

            already_exist = checkIsExists(Carts, customer_id = customer.id, product_id = product.id)
            if already_exist:
                varian_exist = json.loads(already_exist.varian)
                varian_data = data['varian']
                # check if data already exist with the same varian
                if self.checkVarianExist(varian_data, varian_exist):
                    current_quantity = already_exist.quantity
                    already_exist.quantity += current_quantity
                    already_exist.save()
                
                else:
                    self.saveData(data, product)

            else:
                self.saveData(data, product)

            return SuccessResponse({'message':'data successfully added!'})

        except AssertionError as error:
            return AssertionErrorResponse(str(error))

        except Exception as error:
            print(error)
            return ErrorResponse("Internal Server Error", 500)

    def get(self, request):
        try:
            params = request.GET
            assert 'customer_id' in params and params['customer_id'] != '', "parameter customer_id not found::404"
            customer_id = params['customer_id']
            customer = checkIsExists(Customers, id = int(customer_id))
            assert customer, "customer not found::404"

            carts = Carts.objects.filter(customer_id = customer_id)
            data = getPaginate(request, carts, pageQueryName = 'page', sizeQueryName = 'page_size')
            return SuccessResponse({'data': CartSerializer(data['data'], many=True).data, 'meta': data['meta']})


        except AssertionError as error:
            return AssertionErrorResponse(str(error))

        except Exception as error:
            print(error)
            return ErrorResponse("Internal Server Error", 500)