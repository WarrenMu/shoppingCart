from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username} created on {self.created_at}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in cart {self.cart.id}"
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order of {self.user.username} created on {self.created_at}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in order {self.order.id}"
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name    

class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} in category {self.category.name}"  
    
class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"    
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wishlist of {self.user.username}"  
    
class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} in wishlist {self.wishlist.id}"    
    
class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)

    def __str__(self):
        return f"Payment of {self.amount} for order {self.order.id}"    
    
class Shipment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    shipment_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    tracking_number = models.CharField(max_length=100)

    def __str__(self):
        return f"Shipment for order {self.order.id} with tracking number {self.tracking_number}"        

class Discount(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def __str__(self):
        return f"Discount code {self.code} - {self.discount_percentage}%"
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image_url = models.URLField()

    def __str__(self):
        return f"Image for {self.product.name}"
    
class InventoryRecord(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_changed = models.IntegerField()
    change_date = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=255)

    def __str__(self):
        return f"Inventory change for {self.product.name} on {self.change_date}"

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name    

class SupplierProduct(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supply_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} supplied by {self.supplier.name}"  
    
class TaxRate(models.Model):
    region = models.CharField(max_length=100)
    rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Tax rate for {self.region}: {self.rate}%"
    
class GiftCard(models.Model):
    code = models.CharField(max_length=50, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    issued_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()

    def __str__(self):
        return f"Gift card {self.code} with balance {self.balance}"
    
class ReturnRequest(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Return request for order {self.order.id} - Status: {self.status}"  
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wishlist of {self.user.username}"
    
class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} in wishlist {self.wishlist.id}"
    
class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)

    def __str__(self):
        return f"Payment of {self.amount} for order {self.order.id}"    
    
class Shipment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    shipment_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    tracking_number = models.CharField(max_length=100)

    def __str__(self):
        return f"Shipment for order {self.order.id} with tracking number {self.tracking_number}"    
    
class Discount(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def __str__(self):
        return f"Discount code {self.code} - {self.discount_percentage}%"   
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image_url = models.URLField()

    def __str__(self):
        return f"Image for {self.product.name}" 

class InventoryRecord(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_changed = models.IntegerField()
    change_date = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=255)

    def __str__(self):
        return f"Inventory change for {self.product.name} on {self.change_date}"   
    
class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name    
    
class SupplierProduct(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supply_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} supplied by {self.supplier.name}"  
    
class TaxRate(models.Model):
    region = models.CharField(max_length=100)
    rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Tax rate for {self.region}: {self.rate}%"  
    
class GiftCard(models.Model):
    code = models.CharField(max_length=50, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    issued_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()

    def __str__(self):
        return f"Gift card {self.code} with balance {self.balance}" 
    
class ReturnRequest(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Return request for order {self.order.id} - Status: {self.status}"  
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wishlist of {self.user.username}"  
    
class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} in wishlist {self.wishlist.id}"    
    
class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)

    def __str__(self):
        return f"Payment of {self.amount} for order {self.order.id}"    
    
class Shipment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    shipment_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    tracking_number = models.CharField(max_length=100)

    def __str__(self):
        return f"Shipment for order {self.order.id} with tracking number {self.tracking_number}"    
    
class Discount(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def __str__(self):
        return f"Discount code {self.code} - {self.discount_percentage}%"  

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image_url = models.URLField()

    def __str__(self):
        return f"Image for {self.product.name}"
    
class InventoryRecord(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_changed = models.IntegerField()
    change_date = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=255)

    def __str__(self):
        return f"Inventory change for {self.product.name} on {self.change_date}"    

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name    
    
class SupplierProduct(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supply_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} supplied by {self.supplier.name}"  

class TaxRate(models.Model):
    region = models.CharField(max_length=100)
    rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Tax rate for {self.region}: {self.rate}%"  
    
class GiftCard(models.Model):
    code = models.CharField(max_length=50, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    issued_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()

    def __str__(self):
        return f"Gift card {self.code} with balance {self.balance}" 
    
class ReturnRequest(models.Model):  
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Return request for order {self.order.id} - Status: {self.status}"


