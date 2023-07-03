from django.urls import path
from .views import UserRegister,details,show_cart,place_order,change_details,thankyou,delete_from_cart,cart_to_details,buy_now
urlpatterns=[
    path('userregister/',UserRegister),
    path('details/<int:id>/',details),
    path('cart/',show_cart),
    path('buynow/1/<int:id>/',change_details),
    path('buynow/2/<int:id>/',buy_now),
    path('buynow/3/<int:id>/',place_order),
    path('thankyou/',thankyou),
    path('deletefromcart/<int:id>/',delete_from_cart),
    path('details/<str:name>/',cart_to_details)
]