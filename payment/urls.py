from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('confirm_order/', views.confirm_order, name='confirm_order'),
    path('process_order/', views.process_order, name='process_order'),
    path('check_payment/', views.check_payment, name='check_payment'),
]
