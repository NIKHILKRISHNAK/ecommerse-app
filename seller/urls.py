from django.urls import path
from .views import *
urlpatterns=[
    path('',landing),
    path('items/',items),
    path('details/<int:id>',details),
    path('createitem/',create_item),
    path('update/<int:id>',update),
    path('delete/<int:id>',delete),
    path('create-seller/',create_seller)
]