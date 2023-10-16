from django.contrib import admin
from django.urls import path
from MyApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.store, name='landing_page'),  # This sets the store view as the landing page
    path('admin/', admin.site.urls),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('store/', views.store, name="store"),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail_view, name='product_detail'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('thank-you/', views.thank_you, name='thank_you')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
