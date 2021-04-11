from django.urls import path
from .views.user import CustomerView

urlpatterns = [
    path('customers/', CustomerView.as_view())
]