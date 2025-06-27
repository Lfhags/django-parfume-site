import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order
from .tasks import payment_completed
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
        logger.info(f"Webhook event received: {event['type']}")
    except ValueError as e:
        logger.error(f"Invalid payload: {e}")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Invalid signature: {e}")
        return HttpResponse(status=400)
    
    if event['type'] == 'checkout.session.completed':
        session = event.data.object
        logger.info(f"Processing completed session: {session.id}")
        
        if session.mode == 'payment' and session.payment_status == 'paid':
            order_id = session.client_reference_id
            try:
                order = Order.objects.get(id=order_id)
                logger.info(f"Updating order {order_id} as paid")
                order.paid = True
                order.stripe_id = session.payment_intent
                order.save()
                payment_completed.delay(order.id)
                logger.info(f"Order {order_id} marked as paid successfully")
            except Order.DoesNotExist:
                logger.error(f"Order {order_id} not found")
                return HttpResponse(status=404)
            except Exception as e:
                logger.error(f"Error updating order {order_id}: {e}")
                return HttpResponse(status=500)
        else:
            logger.warning(f"Session {session.id} not paid or wrong mode")

    return HttpResponse(status=200)