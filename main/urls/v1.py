from django.urls import path
from ..views.user import CustomerView, SellersView, MerchantView
from ..views.product import UploadProductMediaView, MerchantCategoryView, ProductView

urlpatterns = [
    path('customers/', CustomerView.as_view()),
    path('sellers/', SellersView.as_view()),
    path('merchants/', MerchantView.as_view()),
    path('merchants/<int:id>/categories/', MerchantCategoryView.as_view()),
    path('products/', ProductView.as_view()),
    path('products/media/', UploadProductMediaView.as_view()),
]