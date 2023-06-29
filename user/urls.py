from django.urls import path
from .views import UserRegister,details
urlpatterns=[
    path('userregister/',UserRegister),
    path('details/<int:id>',details)
]