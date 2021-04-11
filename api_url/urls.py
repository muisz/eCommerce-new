from django.urls import path, include

urlpatterns = [
    path('1.0/', include('main.urls.v1'))
]