from django.urls import path
from .views import UserRegister,details,show_cart,buy_now,change_details
urlpatterns=[
    path('userregister/',UserRegister),
    path('details/<int:id>',details),
    path('cart/',show_cart),
    path('buynow/1/<int:id>',change_details),
    path('buynow/2/<int:id>',buy_now)
]