from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError

from .models import Product, Cart, CartItem, Order, OrderItem, Category, Review
from .services import calculate_cart_total, clear_user_cart

# Create your views here.
class HomeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Welcome to the Shop API"})

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Implement checkout logic here
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            return Response({"error": "Cart is empty"}, status=400)

        total_price = calculate_cart_total(cart)
        order = Order.objects.create(user=request.user, total_price=total_price)

        for item in CartItem.objects.filter(cart=cart):
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        clear_user_cart(cart)
        return Response({"message": "Checkout successful"})

class ProductListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.all()
        product_data = [{"id": p.id, "name": p.name, "description": p.description, "price": p.price, "stock": p.stock} for p in products]
        return Response(product_data)

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        items = CartItem.objects.filter(cart=cart)
        item_data = [{"product_id": item.product.id, "quantity": item.quantity} for item in items]
        total_price = calculate_cart_total(cart)
        return Response({"items": item_data, "total_price": total_price})

    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)

        try:
            product = Product.objects.get(id=product_id)
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            cart_item.quantity += quantity
            cart_item.save()
            return Response({"message": "Item added to cart"})
        except Product.DoesNotExist:
            return Response({"error": "Product does not exist"}, status=400)
        except ValidationError as e:
            return Response({"error": str(e)}, status=400)
        
    def delete(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            clear_user_cart(cart)
            return Response({"message": "Cart cleared"})
        except Cart.DoesNotExist:
            return Response({"error": "Cart does not exist"}, status=400)
        
class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            return Response({"error": "Cart is empty"}, status=400)

        total_price = calculate_cart_total(cart)
        order = Order.objects.create(user=request.user, total_price=total_price)

        for item in CartItem.objects.filter(cart=cart):
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        clear_user_cart(cart)
        return Response({"message": "Order placed successfully", "order_id": order.id})

class CategoryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.all()
        category_data = [{"id": c.id, "name": c.name, "description": c.description} for c in categories]
        return Response(category_data)

class ReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        rating = request.data.get("rating")
        comment = request.data.get("comment", "")

        try:
            product = Product.objects.get(id=product_id)
            review = Review.objects.create(
                product=product,
                user=request.user,
                rating=rating,
                comment=comment
            )
            return Response({"message": "Review submitted successfully", "review_id": review.id})
        except Product.DoesNotExist:
            return Response({"error": "Product does not exist"}, status=400)
        except ValidationError as e:
            return Response({"error": str(e)}, status=400)
        
    