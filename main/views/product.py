from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models.user import Customers, CustomerAddress, Sellers, Merchants
from ..models.product import Products, ProductSpecifications, ProductTags, Categories, Orders, Promo, Vouchers
from ..serializers import CustomerSerializer, CustomerAddressSerializer, SellerSerializer, MerchantSerializer, CategorySerializer, ProductSerializer
from utils.response import AssertionErrorResponse, ErrorResponse, SuccessResponse
from utils.utils import generateHash, checkIsExists, getPaginate
import json
import uuid
import os

def saveFile(fileObj):
	try:
		base_dir = settings.MEDIA_ROOT + os.sep + 'products'
		name = fileObj.name.split('.')
		extension = name[len(name)-1]
		filename = '{}.{}'.format(str(uuid.uuid4()), extension)
		
		if not os.path.exists(base_dir):
			os.mkdir(base_dir)

		with open(base_dir + os.sep + filename, 'wb+') as file:
			file.write(fileObj.read())
		
		return settings.MEDIA_URL + 'products/' + filename
	except:
		return False


class UploadProductMediaView(APIView):
	# Content-Type: multipart-formdata
	def post(self, request):
		try:
			data = request.data
			data_length = data['length']
			path = []
			for i in range(int(data_length)):
				attribute = 'file_{}'.format(i+1)
				file = data[attribute]
				print(file)
				saved = saveFile(file)
				print('saved file -> ', saved)
				if saved:
					path.append(saved)

			return SuccessResponse({"data": path})

		except AssertionError as error:
			return AssertionErrorResponse(str(error))

class MerchantCategoryView(APIView):
	def post(self, request, id):
		try:
			data = request.data
			merchant = checkIsExists(Merchants, id = id)
			assert merchant, "merchant id is not found::404"
			saved = Categories.objects.create(merchant_id = id, name = data['name'])
			return SuccessResponse({"message":"data successfully created!"})

		except AssertionError as error:
			return AssertionErrorResponse(str(error))

	def get(self, request, id):
		try:
			params = request.GET
			if 'ouput' in params and params['ouput'] == 'data':
				pass

			categories = Categories.objects.filter(merchant_id = id)
			paginated = getPaginate(request, categories, pageQueryName='page', sizeQueryName='page_size')
			data = CategorySerializer(paginated['data'], many=True).data
			return SuccessResponse({"data":data, "meta": paginated['meta']})


		except AssertionError as error:
			return AssertionErrorResponse(str(error))

class ProductView(APIView):
	def post(self, request):
		try:
			data = request.data
			merchant = checkIsExists(Merchants, id = data['merchant_id'])
			category = checkIsExists(Categories, id = data['category_id'])

			assert merchant, "merchant_id is not found::404"
			assert category, "caregory_id is not found::404"

			product = None
			product_spec = []
			product_tags = []
			try:
				product = Products.objects.create(
					merchant_id = data['merchant_id'],
					name = data['name'],
					description = data['description'],
					price = data['price'],
					stocks = data['stocks'],
					category_id = data['category_id'],
					varian = json.dumps(data['varian']),
					media = json.dumps(data['media'])	
				)

				if 'specifications' in data:
					specifications = data['specifications']
					if not isinstance(specifications, list):
						specifications = json.loads(specifications)
					for spec in specifications:
						try:
							temp = ProductSpecifications.objects.create(
								product_id = product.id,
								name = spec['name'],
								value = spec['value']
							)
							product_spec.append(temp)
						except:
							pass

				if 'tags' in data:
					tags = data['tags']
					if not isinstance(tags, list):
						tags = json.loads(tags)
					for tag in tags:
						try:
							temp = ProductTags.objects.create(
								product_id = product.id,
								name = tag['name']
							)
							product_tags.append(temp)

						except:
							pass

				return SuccessResponse({"message":"data successfully created"})

			except Exception as error:
				if product != None:
					product.delete()

				if len(product_spec) > 0:
					for i in product_spec:
						i.delete()

				if len(product_tags) > 0:
					for i in product_tags:
						i.delete()
				
				print(str(error))
				raise AssertionError("error while submitting data::400")

		except AssertionError as error:
			return AssertionErrorResponse(str(error))

		except:
			return ErrorResponse("BadRequest")

	# def get(self, request):