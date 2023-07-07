from django.urls import path
from .views import *
urlpatterns=[
    path('userregister/',UserRegister),
    path('details/<int:id>/',details),
    path('cart/',show_cart),
    path('buynow/1/<int:id>/',change_details),
    path('buynow/2/<int:id>/',payment),
    path('buynow/3/<int:id>/',place_order),
    path('thankyou/',thankyou),
    path('deletefromcart/<int:id>/',remove_item_from_cart),
    path('details/<str:name>/',cart_to_details),
    path('upi/<int:id>/',upi),
    path('net-banking/<int:id>/',net_banking),
    path('cash-on-delivery/<int:id>/',cash_on_delivery)
    
]