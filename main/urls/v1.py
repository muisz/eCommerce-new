from django.urls import path
from ..views.user import CustomerView, SellersView, MerchantView, CartView
from ..views.product import UploadProductMediaView, MerchantCategoryView, ProductView, ProductDetailView

urlpatterns = [
    path('customers/', CustomerView.as_view()),
    path('carts/', CartView.as_view()),
    path('sellers/', SellersView.as_view()),
    path('merchants/', MerchantView.as_view()),
    path('merchants/<int:id>/categories/', MerchantCategoryView.as_view()),
    path('products/', ProductView.as_view()),
    path('products/media/', UploadProductMediaView.as_view()),
    path('products/<int:id>/', ProductDetailView.as_view())
]