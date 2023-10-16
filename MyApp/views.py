from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, CartItem
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import AnonymousUser

def cart(request):
    if request.user.is_authenticated:
        # Retrieve the user's cart items
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        # Handle anonymous user's cart from session data
        cart = request.session.get('cart', {})
        product_ids = cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        
        cart_items = []
        total_price = 0

        for product in products:
            cart_item = CartItem(product=product, quantity=cart[str(product.id)]['quantity'])
            cart_items.append(cart_item)
            total_price += cart_item.total

    context = {'cart_items': cart_items, 'total_price': total_price}
    return render(request, 'cart.html', context)

@csrf_protect
def checkout(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            # Handle the checkout logic for an authenticated user
            # You can implement order processing and payment logic here
            # For demonstration, clear the user's shopping cart
            CartItem.objects.filter(user=request.user).delete()
        else:
            # Handle anonymous user's cart from session data
            cart = request.session.get('cart', {})
            # You can process the anonymous user's order here
            # Clear the session data or perform any other required actions
            request.session['cart'] = {}

        # Add a success message
        messages.success(request, 'Your order was successfully placed. Thank you for shopping with us!')

        # Redirect to the thank you page or any other page you prefer
        return redirect('thank_you')  # You should define a URL for the thank you page

    # If it's a GET request, render the checkout page
    context = {}
    return render(request, 'checkout.html', context)

# Define your 'thank_you' view here
def thank_you(request):
    # Assuming the order was successful
    messages.success(request, "Thank you for shopping with us!")
# Redirect to the thank you page
    return render(request, 'thank_you.html')
    
def store(request):
    context = {}
    return render(request, 'store.html', context)

def product_list(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'product_list.html', context)

def product_detail_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {'product': product}
    return render(request, 'product_detail.html', context)

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    if request.user.is_authenticated:
        # Add the item to the authenticated user's cart
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += 1
        cart_item.total = cart_item.quantity * cart_item.product.price  # Calculate the total
        cart_item.save()
    else:
        # Handle anonymous user's cart using session data
        cart = request.session.get('cart', {})
        cart_item = cart.get(str(product.id))
        if cart_item is not None:
            cart_item['quantity'] += 1
            cart_item['total'] = cart_item['quantity'] * product.price  # Calculate the total
        else:
            cart[product.id] = {
                'id': product.id,
                'quantity': 1,
                'total': product.price,  # Calculate the total for the first item
            }
        request.session['cart'] = cart
    
    # Redirect to the product listing page
    return redirect('product_list')
