from django.contrib import admin
from .models import Discount, GiftCard, InventoryRecord, Payment, Product, Cart, CartItem, Order, OrderItem, Category, ProductCategory, ProductImage, ReturnRequest, Review, Shipment, Supplier, SupplierProduct, TaxRate, Wishlist, WishlistItem 

# Register your models here.

admin.site.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')
    search_fields = ('name',)

admin.site.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username',)

admin.site.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    search_fields = ('cart__user__username', 'product__name')

admin.site.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'created_at')
    search_fields = ('user__username',)

admin.site.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('order__user__username', 'product__name')

admin.site.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    search_fields = ('product__name', 'user__username')

admin.site.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_email')
    search_fields = ('name',)

admin.site.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'category')
    search_fields = ('product__name', 'category__name')

admin.site.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username',)

admin.site.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('wishlist', 'product')
    search_fields = ('wishlist__user__username', 'product__name')

admin.site.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount', 'payment_method', 'status', 'created_at')
    search_fields = ('order__user__username', 'payment_method', 'status')

admin.site.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('order', 'shipment_date', 'delivery_date', 'status')
    search_fields = ('order__user__username', 'status')

admin.site.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('code', 'amount', 'is_active')
    search_fields = ('code',)

admin.site.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_url')
    search_fields = ('product__name',)

admin.site.register(InventoryRecord)
class InventoryRecordAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'last_updated')
    search_fields = ('product__name',)

admin.site.register(SupplierProduct)
class SupplierProductAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'product', 'supply_price')
    search_fields = ('supplier__name', 'product__name')

admin.site.register(TaxRate)
class TaxRateAdmin(admin.ModelAdmin):
    list_display = ('region', 'rate')
    search_fields = ('region',)

admin.site.register(GiftCard)
class GiftCardAdmin(admin.ModelAdmin):
    list_display = ('code', 'amount', 'is_active')
    search_fields = ('code',)

admin.site.register(ReturnRequest)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')
    search_fields = ('name',)