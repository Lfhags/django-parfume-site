from django.shortcuts import render, redirect, get_object_or_404, reverse
import stripe
from decimal import Decimal
from django.conf import settings
from orders .models import Order
import logging

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def payment_process(request):
    order_id = request.session.get('order_id', None)
    if not order_id:
        logger.error("No order_id in session")
        return redirect('orders:order_create')
    
    order = get_object_or_404(Order, id=order_id)
    logger.info(f"Processing payment for order {order.id}")
    
    if request.method == 'POST':
        success_url = request.build_absolute_uri(
            reverse('payment:completed')
            )
        cancel_url = request.build_absolute_uri(
            reverse('payment:canceled')
            )
        session_data = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': [],
        }
        
        # Додаємо товари до сесії
        for item in order.items.all():
            session_data['line_items'].append({
                'price_data' : {
                    'unit_amount': int(item.price * Decimal(100)),
                    'currency' : 'usd',
                    'product_data' : {
                        'name' : item.product.name,
                        },
                },
                'quantity': item.quantity,})
        
        # Створюємо купон тільки один раз, якщо він є
        if order.coupon:
            try:
                logger.info(f"Creating Stripe coupon for {order.coupon.code}")
                stripe_coupon = stripe.Coupon.create(
                    name = order.coupon.code,
                    percent_off=order.discount,
                    duration='once',)
                session_data['discounts'] = [{
                    'coupon': stripe_coupon.id,
                }]
            except stripe.error.StripeError as e:
                logger.warning(f"Stripe coupon creation failed: {e}")
                # Якщо купон вже існує, використовуємо його
                try:
                    existing_coupons = stripe.Coupon.list(limit=100)
                    for coupon in existing_coupons.data:
                        if coupon.name == order.coupon.code:
                            session_data['discounts'] = [{
                                'coupon': coupon.id,
                            }]
                            logger.info(f"Using existing coupon {coupon.id}")
                            break
                except Exception as e2:
                    logger.error(f"Failed to find existing coupon: {e2}")
        
        try:
            logger.info(f"Creating Stripe session for order {order.id}")
            session = stripe.checkout.Session.create(**session_data)
            logger.info(f"Stripe session created: {session.id}")
            return redirect(session.url, code=303)
        except stripe.error.StripeError as e:
            logger.error(f"Stripe session creation failed: {e}")
            error_message = str(e)
            return render(request, 'payment/process.html', {
                'order': order,
                'error_message': error_message
            })
    else:
        return render(request, 'payment/process.html', locals())
    

def payment_completed(request):
    logger.info("Payment completed successfully")
    return render(request, 'payment/completed.html')


def payment_canceled(request):
    logger.info("Payment was canceled")
    return render(request, 'payment/canceled.html')