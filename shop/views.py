from django.http import JsonResponse
from shop.form import CustomUserForm
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required  
from django.shortcuts import get_object_or_404, render, redirect
from . models import *
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from .utils import generate_invoice
from django.contrib.auth import authenticate,login,logout
import json

def home(request):
    products=Product.objects.filter(trending=1)
    return render(request, "shop/index.html", {"products": products})

def favviewpage(request):
    if request.user.is_authenticated:
        fav=Favourite.objects.filter(user=request.user)
        return render(request, "shop/fav.html", {"fav": fav})
    else:
        return redirect('/')
    
def remove_fav(request, fid):
    fav_item = Favourite.objects.get(id=fid)
    fav_item.delete()
    return redirect('/favviewpage')

def cart_page(request):
    if request.user.is_authenticated:
        
        # 🔥 VERY IMPORTANT
        if 'buy_now' in request.session:
            del request.session['buy_now']
            
        cart=Cart.objects.filter(user=request.user)
        return render(request, "shop/cart.html", {"cart": cart})
    else:
        return redirect('/')

def buy_now(request):
    if not request.user.is_authenticated:
        return JsonResponse({"login_required": True})

    data = json.loads(request.body)
    pid = data['pid']
    qty = int(data['qty'])

    product = Product.objects.get(id=pid)

    request.session['buy_now'] = {
        'product_id': product.id,
        'qty': qty
    }

    return JsonResponse({"login_required": False})

@ensure_csrf_cookie
@login_required
def checkout(request):

    buy_now = request.session.get('buy_now')
    items = []
    total = 0

    if buy_now:
        # 🟢 BUY NOW FLOW
        product = Product.objects.get(id=buy_now['product_id'])
        qty = buy_now['qty']
        cart_items = []

        items.append({
            'product': product,
            'qty': qty,
            'total': product.selling_price * qty
        })

        total = product.selling_price * qty

    else:
        # 🟢 CART FLOW
        cart_items = Cart.objects.filter(user=request.user)
        
        if not cart_items.exists():
            messages.warning(request, "Your cart is empty. Please add items to proceed to checkout.")
            return redirect('cart')

        for c in cart_items:
            items.append({
                'product': c.product,
                'qty': c.product_qty,
                'total': c.product.selling_price * c.product_qty
            })
            total += c.product.selling_price * c.product_qty

    addresses = Address.objects.filter(user=request.user)

    response = render(request, 'shop/checkout.html', {
        'items': items,
        'total': total,
        'addresses': addresses
    })
    return response

@login_required
@csrf_protect
def save_address(request):
    
    # ❌ GET request வந்தா
    if request.method != "POST":
        return redirect('checkout')   # or HttpResponseBadRequest("Invalid request")

    address_id = request.POST.get("address_id")
    full_name = request.POST.get("full_name")
    phone = request.POST.get("phone")
    address = request.POST.get("address_line")
    city = request.POST.get("city")
    state = request.POST.get("state")
    pincode = request.POST.get("pincode")

    if address_id:
        # EDIT address
        addr = Address.objects.get(id=address_id, user=request.user)
        addr.full_name = full_name
        addr.phone = phone
        addr.address_line = address
        addr.city = city
        addr.state = state
        addr.pincode = pincode
        addr.save()
    else:
        # ADD new address
        Address.objects.create(
            user=request.user,
            full_name=full_name,
            phone=phone,
            address_line=address,
            city=city,
            state=state,
            pincode=pincode
        )

    # ✅ MUST RETURN RESPONSE
    return redirect('checkout')
    
@login_required
@csrf_protect
def place_order(request):
    if request.method != "POST":
        return JsonResponse({"status": False})

    data = json.loads(request.body)
    address_id = data.get("address_id")
    payment_mode = data.get("payment_mode")
    
    # 🔥 ONLINE PAYMENT
    if payment_mode == "ONLINE":
        return JsonResponse({
            "redirect_url": f"/payment/?address_id={address_id}"
        })

    # 🔥 COD PAYMENT
    buy_now = request.session.get('buy_now')
    
    if buy_now:
        product = Product.objects.get(id=buy_now['product_id'])
        qty = buy_now['qty']
        total = product.selling_price * qty
        
        order=Order.objects.create(
            user=request.user,
            address_id=address_id,
            total_price=total,
            payment_mode="COD",
            payment_status="PENDING"
        )
        
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=qty,
            price=product.selling_price
        )
        product.quantity -= qty
        product.save()
        del request.session['buy_now']
        
    else:
        cart = Cart.objects.filter(user=request.user) 
        total = sum(c.product.selling_price * c.product_qty for c in cart)
        
        order = Order.objects.create(
            user=request.user,
            address_id=address_id,
            total_price=total,
            payment_mode="COD",
            payment_status="PENDING",
            status="PLACED",
            placed_at=timezone.now()
        )
        
        for c in cart: 
            OrderItem.objects.create( 
                order=order, 
                product=c.product, 
                quantity=c.product_qty, 
                price=c.product.selling_price 
            )
             
            c.product.quantity -= c.product_qty 
            c.product.save() 
            
        cart.delete() 
            
    return JsonResponse({
        "redirect_url": "/order-success/",
        "status": "Order Placed Successfully"
    })

def address_page(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
        Address.objects.create(
            user=request.user,
            full_name=request.POST.get('full_name'),
            phone=request.POST.get('phone'),
            address_line=request.POST.get('address'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            pincode=request.POST.get('pincode'),
        )
        messages.success(request, "Address added successfully")
        return redirect('address')

    addresses = Address.objects.filter(user=request.user)
    return render(request, 'shop/address.html', {'addresses': addresses})

def remove_cart(request, cid):
    cart_item = Cart.objects.get(id=cid)
    cart_item.delete()
    return redirect('/cart')

@login_required
@csrf_protect
def fav_page(request):
    if request.method == "POST":

        if not request.user.is_authenticated:
            return JsonResponse({'status': 'Login to Add Favourite'})

        try:
            data = json.loads(request.body)
            product_id = data.get('pid')
            product = Product.objects.get(id=product_id)

            if Favourite.objects.filter(user=request.user, product=product).exists():
                return JsonResponse({'status': 'Product Already in Favourite'})

            Favourite.objects.create(
                user=request.user,
                product=product
            )

            return JsonResponse({'status': 'Product Added to Favourite'})

        except Exception:
            return JsonResponse({'status': 'Something went wrong'})

    return JsonResponse({'status': 'Invalid Request'})

@login_required
@csrf_protect
def add_to_cart(request):
    if request.method != "POST":
        return JsonResponse({'status': 'Invalid Request'})

    if not request.user.is_authenticated:
        return JsonResponse({'status': 'Login to Add Cart'})

    try:
        data = json.loads(request.body)

        product_id = data.get('pid')
        product_qty = int(data.get('product_qty'))

        product = Product.objects.get(id=product_id)

        if Cart.objects.filter(user=request.user, product=product).exists():
            return JsonResponse({'status': 'Product Already in Cart'})

        if product.quantity < product_qty:
            return JsonResponse({'status': 'Product Stock Not Available'})

        Cart.objects.create(
            user=request.user,
            product=product,
            product_qty=product_qty
        )

        return JsonResponse({'status': 'Product Added to Cart'})

    except Exception as e:
        print("ADD TO CART ERROR 👉", e)
        return JsonResponse({'status': 'Something went wrong'})

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out Successfully")
    return redirect("/")

def login_page(request):
    if request.method=='POST':
        name=request.POST.get('username')
        pwd=request.POST.get('password')
        user=authenticate(request,username=name,password=pwd)
        if user is not None:
            login(request,user)
            messages.success(request,"Logged in Successfully")
            return redirect("/")
        else:
            messages.error(request,"Invalid User Name or Password")
            return redirect("/login")
        
    return render(request, "shop/login.html")

def register(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration Success You Can Login Now..!")
            return redirect('/login')
    return render(request, "shop/register.html",{'form':form})

def collections(request):
    category=Category.objects.filter(status=0)
    return render(request, "shop/collections.html", {"category": category})

def collectionsview(request, name):
    if(Category.objects.filter(name=name, status=0)):
        products=Product.objects.filter(category__name=name)
        return render(request, "shop/products/index.html", {"products": products, "category_name": name})
    else:
        messages.warning(request, "No Such Category Found")
        return redirect('collections')
    
@ensure_csrf_cookie
def product_details(request, cname, pname):
    if(Category.objects.filter(name=cname, status=0)):
        if(Product.objects.filter(name=pname, status=0)):
            products=Product.objects.filter(name=pname, status=0).first()
            return render(request, "shop/products/product_details.html", {"products": products})
        else:
            messages.error(request, "No Such Product Found")
            return redirect('collections')
    else:
        messages.error(request, "No Such Category Found")
        return redirect('collections')
    
def product_detail_by_id(request, id):
    product = Product.objects.get(id=id, status=0)
    return render(request, "shop/products/product_details.html", {
        "products": product
    })
    
def search(request):
    query = request.GET.get('q')
    category_slug = request.GET.get('category')

    products = Product.objects.filter(status=0)

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    if category_slug and category_slug != "":
        products = products.filter(category__slug__iexact=category_slug)
        print("CATEGORY:", category_slug)

    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'shop/search.html', context)

def search_suggestions(request):
    term = request.GET.get('term', '')
    category = request.GET.get('category', '')

    products = Product.objects.filter(status=0)

    if term:
        products = products.filter(name__icontains=term)

    if category:
        products = products.filter(category__name__iexact=category)

    products = products[:6]

    results = []
    for p in products:
        results.append({
            "name": p.name,
            "price": p.selling_price,
            "image": p.product_image.url if p.product_image else "",
            "url": reverse('product_detail_by_id', args=[p.id])
        })

    return JsonResponse(results, safe=False)

def product_list(request):
    category = request.GET.get('category')
    query = request.GET.get('query')

    products = Product.objects.filter(status=0)
    selected_category = category
    last_product = None

    if query:
        products = products.filter(name__icontains=query)

        # 🔥 AUTO CATEGORY SET
        if not category and products.exists():
            selected_category = products.first().category.name

    if selected_category:
        products = products.filter(category__name=selected_category)
        
    if products.exists():
        last_product = products.first().name 
        
    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': selected_category,
        'last_product': last_product,
    }
    return render(request, 'shop/product_list.html', context)

def product_page(request):
    if request.user.is_staff:
        return redirect('/admin/')
    return render(request, 'shop/product_list.html')

@login_required
@csrf_protect
def payment(request):
        address_id = request.GET.get("address_id")
        if not address_id:
            return redirect("checkout")

        return render(request, "shop/payment.html", {
            "address_id": address_id
        })

@login_required
@csrf_protect
def payment_success(request):

    address_id = request.POST.get("address_id")
    payment_mode = request.POST.get("payment_mode")
    buy_now = request.session.get("buy_now")

    # 🔥 BUY NOW FLOW
    if buy_now:
        product = Product.objects.get(id=buy_now["product_id"])
        qty = buy_now["qty"]
        total = product.selling_price * qty

        order = Order.objects.create(
            user=request.user,
            address_id=address_id,
            total_price=total,
            upi_app=request.POST.get("upi_app"),
            payment_mode="ONLINE",
            status="PLACED",
            payment_status="SUCCESS"
        )

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=qty,
            price=product.selling_price
        )

        product.quantity -= qty
        product.save()

        # 🔥 VERY IMPORTANT
        del request.session["buy_now"]

        return redirect("order_success")

    # 🔥 CART FLOW
    cart = Cart.objects.filter(user=request.user)

    total = sum(c.product.selling_price * c.product_qty for c in cart)

    order = Order.objects.create(
        user=request.user,
        address_id=address_id,
        total_price=total,
        upi_app=request.POST.get("upi_app"),
        payment_mode="ONLINE",
        status="PLACED",
        payment_status="SUCCESS"
    )

    for c in cart:
        OrderItem.objects.create(
            order=order,
            product=c.product,
            quantity=c.product_qty,
            price=c.product.selling_price
        )

        c.product.quantity -= c.product_qty
        c.product.save()

    cart.delete()

    return redirect("order_success", order_id=order.id)

@login_required
def order_success(request):
    order = Order.objects.filter(user=request.user).last()
    return render(request, "shop/order_success.html", {"order": order})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("items__product").order_by('-created_at')
    return render(request, "shop/my_orders.html", {
        "orders": orders
    })
    
@login_required
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)

    return render(request, "shop/order_details.html", {
        'order': order,
        'order_items': order_items,
        'address': order.address   # 🔥 ADD THIS
    })

def cancel_order(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)

    if order.status != "PLACED":
        messages.error(request, "❌ This order cannot be cancelled now.")
        return redirect("order_details", order_id=order.id)

    order.status = "CANCELLED"
    order.cancelled_at = timezone.now()
    order.save()

    messages.success(request, "✅ Order cancelled successfully.")
    return redirect("my_orders")

@staff_member_required
def admin_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, "shop/admin_orders.html", {
        "orders": orders
    })
    
@staff_member_required
def admin_order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "shop/admin_order_details.html", {
        'order': order,
        'address': order.address
    })
    
@staff_member_required
def update_order_status(request, order_id):
    if not request.user.is_staff:
        return redirect("home")
    
    order = Order.objects.get(id=order_id)
    
    if request.method == "POST":
        status = request.POST.get("status")
        order.status = status
        
        if status == "SHIPPED":
            order.shipped_at = timezone.now()
                
        elif status == "OUT_FOR_DELIVERY":
            order.out_for_delivery_at = timezone.now()
                
        elif status == "DELIVERED":
            order.delivered_at = timezone.now()
                
        elif status == "CANCELLED":
            order.cancelled_at = timezone.now()
                
        order.save()
            
    return redirect('admin_order_details', order_id=order.id)

@login_required
def download_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return generate_invoice(order)
