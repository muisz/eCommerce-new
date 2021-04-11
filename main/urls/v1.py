from django.urls import path
from ..views.user import CustomerView, SellersView

urlpatterns = [
    path('customers/', CustomerView.as_view()),
    path('sellers/', SellersView.as_view())
]