from functools import reduce
from django.core.exceptions import ValidationError
from .models import CartItem, Order

_order = Order
_cartItem = CartItem

UGX_DENOMS = [50000, 20000, 10000, 5000, 2000, 1000, 500, 200, 100] # Ugandan Shillings

def validate_ugx_amount(amount: int) -> None:
    """ Validates that the given amount can be represented using UGX denominations. """
    if amount < 0:
        raise ValidationError("Amount cannot be negative.")
    
    remaining = amount
    for denom in UGX_DENOMS:
        count = remaining // denom
        remaining -= count * denom
    
    if remaining != 0:
        raise ValidationError(f"Amount {amount} cannot be represented using UGX denominations.")
    
def calculate_change(amount_paid: int, total_cost: int) -> dict[int, int]:
    """ Calculates the change to be given using the least number of UGX denominations. """
    if amount_paid < total_cost:
        raise ValidationError("Amount paid is less than total cost.")
    
    change_to_give = amount_paid - total_cost
    change_distribution = {}
    
    for denom in UGX_DENOMS:
        count = change_to_give // denom
        if count > 0:
            change_distribution[denom] = count
            change_to_give -= count * denom
    
    return change_distribution

def calculate_order_total(order: _order) -> float:
    """ Calculates the total amount for the given order. """
    total = sum(item.product.price * item.quantity for item in order.items.all())
    return total

def calculate_cart_total(cart_items: list[_cartItem]) -> float:
    """ Calculates the total amount for the given cart items. """
    total = sum(item.product.price * item.quantity for item in cart_items)
    return total

def clear_cart(cart_items: list[_cartItem]) -> None:
    """ Clears the given cart items. """
    for item in cart_items:
        item.delete()

def get_cart_items_by_user(user_id: int) -> list[_cartItem]:
    """ Retrieves cart items for the given user ID. """
    return list(CartItem.objects.filter(cart__user__id=user_id).select_related("product"))

def get_order_by_id(order_id: int) -> _order | None:
    """ Retrieves an order by its ID. """
    try:
        return Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return None

def get_cart_by_user(user_id: int):
    """ Retrieves a cart by user ID. """
    from .models import Cart
    try:
        return Cart.objects.get(user__id=user_id)
    except Cart.DoesNotExist:
        return None
    
def create_order(user, total_amount: float) -> _order:
    """ Creates a new order for the given user with the specified total amount. """
    order = Order.objects.create(user=user, total_amount=total_amount)
    return order

def add_item_to_cart(cart, product, quantity: int) -> _cartItem:
    """ Adds an item to the cart or updates its quantity if it already exists. """
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()
    return cart_item

def remove_item_from_cart(cart, product) -> None:
    """ Removes an item from the cart. """
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass

def update_item_quantity(cart, product, quantity: int) -> _cartItem:
    """ Updates the quantity of an item in the cart. """
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity = quantity
    cart_item.save()
    return cart_item

def list_cart_items(cart) -> list[_cartItem]:
    """ Lists all items in the cart. """
    return list(CartItem.objects.filter(cart=cart).select_related("product"))

def list_orders_by_user(user_id: int) -> list[_order]:
    """ Lists all orders for the given user ID. """
    return list(Order.objects.filter(user__id=user_id).order_by('-created_at'))

def delete_order(order_id: int) -> bool:
    """ Deletes an order by its ID. Returns True if deleted, False if not found. """
    try:
        order = Order.objects.get(id=order_id)
        order.delete()
        return True
    except Order.DoesNotExist:
        return False

def clear_user_cart(user_id: int) -> None:
    """ Clears the cart for the given user ID. """
    CartItem.objects.filter(cart__user__id=user_id).delete()

def get_total_items_in_cart(cart) -> int:
    """ Gets the total number of items in the cart. """
    return sum(item.quantity for item in CartItem.objects.filter(cart=cart))

def get_total_orders_count() -> int:
    """ Gets the total number of orders in the system. """
    return Order.objects.count()

def get_most_ordered_products(top_n: int) -> list[tuple]:
    """ Gets the top N most ordered products. """
    from django.db.models import Count
    from .models import Product

    return list(
        Product.objects.annotate(order_count=Count('cartitem__cart__order'))
        .order_by('-order_count')[:top_n]
        .values_list('id', 'name', 'order_count')
    )
def get_least_ordered_products(top_n: int) -> list[tuple]:
    """ Gets the top N least ordered products. """
    from django.db.models import Count
    from .models import Product

    return list(
        Product.objects.annotate(order_count=Count('cartitem__cart__order'))
        .order_by('order_count')[:top_n]
        .values_list('id', 'name', 'order_count')
    )

def get_average_order_value() -> float:
    """ Calculates the average order value across all orders. """
    from django.db.models import Avg
    average = Order.objects.aggregate(Avg('total_amount'))['total_amount__avg']
    return average if average is not None else 0.0

def get_total_revenue() -> float:
    """ Calculates the total revenue from all orders. """
    from django.db.models import Sum
    total = Order.objects.aggregate(Sum('total_amount'))['total_amount__sum']
    return total if total is not None else 0.0

def get_user_order_history(user_id: int) -> list[_order]:
    """ Retrieves the order history for a specific user. """
    return list(Order.objects.filter(user__id=user_id).order_by('-created_at'))

def get_cart_total_items_and_amount(cart) -> tuple[int, float]:
    """ Gets the total number of items and total amount in the cart. """
    cart_items = CartItem.objects.filter(cart=cart)
    total_items = sum(item.quantity for item in cart_items)
    total_amount = sum(item.product.price * item.quantity for item in cart_items)
    return total_items, total_amount

def migrate_cart_to_order(cart, order) -> None:
    """ Migrates items from the cart to the order. """
    cart_items = CartItem.objects.filter(cart=cart)
    for item in cart_items:
        order.items.create(
            product=item.product,
            quantity=item.quantity
        )
    cart_items.delete()

def get_orders_within_date_range(start_date, end_date) -> list[_order]:
    """ Retrieves orders placed within a specific date range. """
    return list(Order.objects.filter(created_at__range=(start_date, end_date)).order_by('-created_at'))

def get_top_customers(top_n: int) -> list[tuple]:
    """ Gets the top N customers based on total order amount. """
    from django.db.models import Sum
    from django.contrib.auth.models import User

    return list(
        User.objects.annotate(total_spent=Sum('order__total_amount'))
        .order_by('-total_spent')[:top_n]
        .values_list('id', 'username', 'total_spent')
    )

def get_inactive_carts(threshold_date) -> list:
    """ Retrieves carts that have not been updated since the threshold date. """
    from .models import Cart
    return list(Cart.objects.filter(updated_at__lt=threshold_date))

def delete_inactive_carts(threshold_date) -> int:
    """ Deletes carts that have not been updated since the threshold date. Returns the number of deleted carts. """
    from .models import Cart
    inactive_carts = Cart.objects.filter(updated_at__lt=threshold_date)
    count = inactive_carts.count()
    inactive_carts.delete()
    return count

def get_total_cart_value_by_user(user_id: int) -> float:
    """ Calculates the total value of the cart for a specific user. """
    cart_items = CartItem.objects.filter(cart__user__id=user_id)
    total_value = sum(item.product.price * item.quantity for item in cart_items)
    return total_value  

def apply_discount_to_order(order: _order, discount_percentage: float) -> float:
    """ Applies a discount to the order and returns the new total amount. """
    if not (0 <= discount_percentage <= 100):
        raise ValidationError("Discount percentage must be between 0 and 100.")
    
    discount_amount = (discount_percentage / 100) * order.total_amount
    new_total = order.total_amount - discount_amount
    order.total_amount = new_total
    order.save()
    return new_total

def get_cart_items_count(cart) -> int:
    """ Gets the count of distinct items in the cart. """
    return CartItem.objects.filter(cart=cart).count()

def get_orders_exceeding_amount(amount: float) -> list[_order]:
    """ Retrieves orders that exceed a specific total amount. """
    return list(Order.objects.filter(total_amount__gt=amount).order_by('-total_amount'))

def get_average_items_per_order() -> float:
    """ Calculates the average number of items per order. """
    from django.db.models import Avg, Count
    average = Order.objects.annotate(item_count=Count('items')).aggregate(Avg('item_count'))['item_count__avg']
    return average if average is not None else 0.0

def get_most_expensive_order() -> _order | None:
    """ Retrieves the most expensive order based on total amount. """
    try:
        return Order.objects.order_by('-total_amount').first()
    except Order.DoesNotExist:
        return None
    
def get_least_expensive_order() -> _order | None:
    """ Retrieves the least expensive order based on total amount. """
    try:
        return Order.objects.order_by('total_amount').first()
    except Order.DoesNotExist:
        return None
    
def get_total_quantity_sold_of_product(product_id: int) -> int:
    """ Calculates the total quantity sold of a specific product across all orders. """
    from .models import Product
    try:
        product = Product.objects.get(id=product_id)
        total_quantity = sum(
            item.quantity for item in CartItem.objects.filter(product=product)
        )
        return total_quantity
    except Product.DoesNotExist:
        return 0    
    
def get_orders_containing_product(product_id: int) -> list[_order]:
    """ Retrieves orders that contain a specific product. """
    from .models import Product
    try:
        product = Product.objects.get(id=product_id)
        orders = Order.objects.filter(items__product=product).distinct().order_by('-created_at')
        return list(orders)
    except Product.DoesNotExist:
        return []
    
def get_total_revenue_within_date_range(start_date, end_date) -> float:
    """ Calculates the total revenue from orders placed within a specific date range. """
    from django.db.models import Sum
    total = Order.objects.filter(created_at__range=(start_date, end_date)).aggregate(Sum('total_amount'))['total_amount__sum']
    return total if total is not None else 0.0

def get_average_order_value_within_date_range(start_date, end_date) -> float:
    """ Calculates the average order value for orders placed within a specific date range. """
    from django.db.models import Avg
    average = Order.objects.filter(created_at__range=(start_date, end_date)).aggregate(Avg('total_amount'))['total_amount__avg']
    return average if average is not None else 0.0

def get_top_selling_products(top_n: int) -> list[tuple]:
    """ Gets the top N selling products based on quantity sold. """
    from django.db.models import Sum
    from .models import Product

    return list(
        Product.objects.annotate(total_sold=Sum('cartitem__quantity'))
        .order_by('-total_sold')[:top_n]
        .values_list('id', 'name', 'total_sold')
    )

def get_least_selling_products(top_n: int) -> list[tuple]:
    """ Gets the top N least selling products based on quantity sold. """
    from django.db.models import Sum
    from .models import Product

    return list(
        Product.objects.annotate(total_sold=Sum('cartitem__quantity'))
        .order_by('total_sold')[:top_n]
        .values_list('id', 'name', 'total_sold')
    )

def get_total_products_sold() -> int:
    """ Calculates the total number of products sold across all orders. """
    from django.db.models import Sum
    total = CartItem.objects.aggregate(Sum('quantity'))['quantity__sum']
    return total if total is not None else 0

def get_total_unique_customers() -> int:
    """ Gets the total number of unique customers who have placed orders. """
    from django.contrib.auth.models import User
    return User.objects.filter(order__isnull=False).distinct().count()  

