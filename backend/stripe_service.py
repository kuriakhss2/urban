from fastapi import HTTPException, Request
from emergentintegrations.payments.stripe.checkout import StripeCheckout, CheckoutSessionResponse, CheckoutStatusResponse, CheckoutSessionRequest
import os
from datetime import datetime
from database import db, orders_collection
from payment_models import PaymentTransaction
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class StripePaymentService:
    def __init__(self):
        self.api_key = os.environ.get('STRIPE_API_KEY')
        if not self.api_key:
            raise ValueError("STRIPE_API_KEY environment variable is required")

    def _get_stripe_checkout(self, base_url: str) -> StripeCheckout:
        """Initialize Stripe checkout with webhook URL"""
        webhook_url = f"{base_url}api/webhook/stripe"
        return StripeCheckout(api_key=self.api_key, webhook_url=webhook_url)

    async def create_checkout_session(self, order_id: str, customer_email: str, origin_url: str) -> CheckoutSessionResponse:
        """Create Stripe checkout session for an order"""
        try:
            # Get order from database
            order = await orders_collection.find_one({"id": order_id}, {"_id": 0})
            if not order:
                raise HTTPException(status_code=404, detail="Order not found")

            # Security: Get amount from server-side order, not from frontend
            total_amount = float(order['total'])
            
            # Initialize Stripe checkout
            stripe_checkout = self._get_stripe_checkout(origin_url)
            
            # Build success and cancel URLs using frontend origin
            success_url = f"{origin_url}/checkout/success?session_id={{CHECKOUT_SESSION_ID}}"
            cancel_url = f"{origin_url}/cart"
            
            # Create checkout session request
            checkout_request = CheckoutSessionRequest(
                amount=total_amount,
                currency="usd",
                success_url=success_url,
                cancel_url=cancel_url,
                metadata={
                    "order_id": order_id,
                    "customer_email": customer_email,
                    "source": "urban_threads_checkout"
                }
            )
            
            # Create Stripe checkout session
            session = await stripe_checkout.create_checkout_session(checkout_request)
            
            # Create payment transaction record BEFORE redirecting to Stripe
            payment_transaction = PaymentTransaction(
                session_id=session.session_id,
                amount=total_amount,
                currency="usd",
                customer_email=customer_email,
                payment_status="pending",
                status="initiated",
                metadata={
                    "order_id": order_id,
                    "stripe_session_id": session.session_id
                }
            )
            
            # Store payment transaction in database
            await db.payment_transactions.insert_one(payment_transaction.dict())
            
            logger.info(f"Created Stripe checkout session {session.session_id} for order {order_id}")
            return session
            
        except Exception as e:
            logger.error(f"Error creating checkout session: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to create checkout session: {str(e)}")

    async def get_checkout_status(self, session_id: str, base_url: str) -> Dict[str, Any]:
        """Get checkout session status and update payment transaction"""
        try:
            # Initialize Stripe checkout
            stripe_checkout = self._get_stripe_checkout(base_url)
            
            # Get status from Stripe
            checkout_status: CheckoutStatusResponse = await stripe_checkout.get_checkout_status(session_id)
            
            # Find existing payment transaction
            payment_transaction = await db.payment_transactions.find_one(
                {"session_id": session_id}, {"_id": 0}
            )
            
            if not payment_transaction:
                raise HTTPException(status_code=404, detail="Payment transaction not found")
            
            # Update payment transaction status (only if not already processed)
            if payment_transaction['payment_status'] != 'paid' or payment_transaction['status'] != 'completed':
                update_data = {
                    "payment_status": checkout_status.payment_status,
                    "status": "completed" if checkout_status.payment_status == "paid" else checkout_status.status,
                    "updated_at": datetime.utcnow()
                }
                
                await db.payment_transactions.update_one(
                    {"session_id": session_id},
                    {"$set": update_data}
                )
                
                # If payment is successful, update order status
                if checkout_status.payment_status == "paid":
                    order_id = payment_transaction['metadata'].get('order_id')
                    if order_id:
                        await orders_collection.update_one(
                            {"id": order_id},
                            {"$set": {"status": "paid", "payment_session_id": session_id}}
                        )
                        logger.info(f"Updated order {order_id} status to paid")
            
            return {
                "session_id": session_id,
                "status": checkout_status.status,
                "payment_status": checkout_status.payment_status,
                "amount_total": checkout_status.amount_total,
                "currency": checkout_status.currency,
                "metadata": checkout_status.metadata
            }
            
        except Exception as e:
            logger.error(f"Error getting checkout status: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to get checkout status: {str(e)}")

    async def handle_webhook(self, request_body: bytes, stripe_signature: str, base_url: str):
        """Handle Stripe webhook events"""
        try:
            # Initialize Stripe checkout
            stripe_checkout = self._get_stripe_checkout(base_url)
            
            # Handle webhook
            webhook_response = await stripe_checkout.handle_webhook(request_body, stripe_signature)
            
            # Update payment transaction based on webhook event
            if hasattr(webhook_response, 'session_id') and webhook_response.session_id:
                await self.get_checkout_status(webhook_response.session_id, base_url)
            
            logger.info(f"Processed webhook event: {webhook_response.event_type}")
            return {"status": "success", "event_type": webhook_response.event_type}
            
        except Exception as e:
            logger.error(f"Error handling webhook: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Webhook processing failed: {str(e)}")

# Global stripe service instance
stripe_service = StripePaymentService()