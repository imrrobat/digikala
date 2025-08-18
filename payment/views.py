from django.shortcuts import render, redirect, get_object_or_404
from cart.cart import Cart
from .forms import ShippingForm
from .models import ShippingAddress, Order, OrderItem
from django.contrib import messages
from shop.models import Product, Profile
from django.contrib.auth.models import User 
import requests
from dotenv import load_dotenv
import os 
import uuid
#from django.http import HttpResponse


load_dotenv()
ZARINPAL_MERCHENT = os.getenv('ZARINPAL_MERCHENT')
ZARINPAL_API = "https://payment.zarinpal.com/pg/v4/payment"
CALLBACK_URL = "HERE YOU MUST PUT A CALLBACK URL"

# def payment_success(request):
#     return render(request, 'payment/payment_success.htm', {}) 

def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    total = cart.get_total()
    
    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user__id = request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'payment/checkout.html', {'cart_products':cart_products,'quantities':quantities, 'total':total, 'shipping_form':shipping_form})
    else:
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payment/checkout.html', {'cart_products':cart_products,'quantities':quantities, 'total':total, 'shipping_form':shipping_form})
    

def confirm_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        total = cart.get_total()
        
        user_shipping = request.POST 
        request.session['user_shipping'] = user_shipping 
        
        return render(request, 'payment/confirm_order.htm', {'cart_products':cart_products,'quantities':quantities, 'total':total, 'shipping_info':user_shipping})

    else:
        messages.success(request, 'دسترسی به این صفحه امکان پذیر نمیباشد')
        return redirect('home')
    # return render(request, 'payment/confirm_order.htm', {})

def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        total = cart.get_total()
        
        user_shipping = request.session.get('user_shipping') 
        
        full_name = user_shipping['shipping_full_name']
        email = user_shipping['shipping_email']
        full_address = f"{user_shipping['shipping_address1']}\n{user_shipping['shipping_address2']}\n{user_shipping['shipping_city']}\n{user_shipping['shipping_state']}\n{user_shipping['shipping_zipcode']}\n{user_shipping['shipping_country']}"
        
        uuid_code = str(uuid.uuid4())
        
        if request.user.is_authenticated:
            new_order = Order(
                user=request.user ,
                full_name=full_name,
                email=email,
                shipping_address=full_address,
                amount_paid=total
            )
            
        else:
            new_order = Order(
                full_name=full_name,
                email=email,
                shipping_address=full_address,
                amount_paid=total
            )
        new_order.save()
        
        
        odr = get_object_or_404(Order, id=new_order.pk)
        
        for product in cart_products:
            prod = get_object_or_404(Product, id= product.id)
            price = product.sale_price if product.is_sale else product.price
            
            for k,v in quantities.items():
                if int(k) == product.id:
                    new_item = OrderItem(
                        order = odr,
                        product = prod,
                        price = price,
                        quantity=v,
                        user = request.user if request.user.is_authenticated else None
                    )
                    new_item.save()
        for key in list(request.session.keys()):
            if key == 'session_key':
                del request.session[key]
        if request.user.is_authenticated:
            Profile.objects.filter(user__id=request.user.id).update(old_cart="")
        
        
        # messages.success(request, 'سفارش ثبت شد')
        # return redirect('home')
        CALLBACK_URL = f"https://digikala-vdot.onrender.com/payment/check_payment/?uuid={new_order.uuid}"

        payload = {
            "merchant_id": ZARINPAL_MERCHENT,
            "amount": int(total),
            "callback_url": CALLBACK_URL,
            "description": f"پرداخت سفارش {new_order.id}",
        }
        response = requests.post(f"{ZARINPAL_API}/request.json", json=payload)
        data = response.json().get("data", {})
        
        if data.get("authority"):
            pay_url = f"https://www.zarinpal.com/pg/StartPay/{data['authority']}"
            return render(request, "payment/redirecting.html", {"pay_url": pay_url})
        else:
            #return HttpResponse(response.text)
            messages.error(request, "خطا در اتصال به درگاه پرداخت")
            return redirect("home")
          
    else:
       messages.success(request, 'دسترسی به این صفحه امکان پذیر نمیباشد')
       return redirect('home') 
   
   
def check_payment(request):
    status = request.GET.get("Status")
    authority = request.GET.get("Authority")
    uuid_code = request.GET.get("uuid")

    order = get_object_or_404(Order, uuid=uuid_code)

    context = {
        "success": False,
        "tracking_code": None,
        "message": ""
    }

    if status == "OK":
        payload = {
            "merchant_id": ZARINPAL_MERCHENT,
            "amount": int(order.amount_paid),
            "authority": authority
        }
        response = requests.post(f"{ZARINPAL_API}/verify.json", json=payload)
        data = response.json().get("data", {})

        if data.get("code") in [100, 101]:
            order.status = "Processing"
            order.save()
            context["success"] = True
            context["tracking_code"] = data.get("ref_id")
            context["message"] = "پرداخت با موفقیت انجام شد"
        else:
            order.status = "Failed"
            order.save()
            context["message"] = f"پرداخت ناموفق بود. کد خطا: {data.get('code')}"
    else:
        order.status = "Cancelled"
        order.save()
        context["message"] = "پرداخت توسط کاربر لغو شد"

    return render(request, "payment/payment_status.html", context)


