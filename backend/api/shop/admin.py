from django.contrib import admin
from .models import Discount, GiftCard, InventoryRecord, Payment, Product, Cart, CartItem, Order, OrderItem, Category, ProductCategory, ProductImage, ReturnRequest, Review, Shipment, Supplier, SupplierProduct, TaxRate, Wishlist, WishlistItem 

# Register your models here.

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Supplier)
admin.site.register(ProductCategory)
admin.site.register(Wishlist)
admin.site.register(WishlistItem)
admin.site.register(Payment)
admin.site.register(Shipment)
admin.site.register(Discount)
admin.site.register(ProductImage)
admin.site.register(InventoryRecord)
admin.site.register(SupplierProduct)
admin.site.register(TaxRate)
admin.site.register(GiftCard)
admin.site.register(ReturnRequest)