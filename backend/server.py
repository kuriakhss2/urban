from fastapi import FastAPI, APIRouter, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import logging
from pathlib import Path
from typing import List
from datetime import datetime

# Import models and database
from models import *
from database import *
from email_service import send_custom_order_notification, send_order_confirmation
from payment_models import CheckoutRequest, CheckoutStatusRequest
from stripe_service import stripe_service

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create the main app without a prefix
app = FastAPI(title="Urban Threads API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database with products on startup
@app.on_event("startup")
async def startup_event():
    await init_products()

# Health check
@api_router.get("/")
async def root():
    return {"message": "Urban Threads API is running"}

# Products endpoints
@api_router.get("/products", response_model=List[Product])
async def get_all_products():
    """Get all products"""
    try:
        products = await products_collection.find({}, {"_id": 0}).to_list(1000)
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/products/category/{category}", response_model=List[Product])
async def get_products_by_category(category: str):
    """Get products by category"""
    try:
        products = await products_collection.find(
            {"category": category}, {"_id": 0}
        ).to_list(1000)
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int):
    """Get single product by ID"""
    try:
        product = await products_collection.find_one(
            {"id": product_id}, {"_id": 0}
        )
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Orders endpoints
@api_router.post("/orders", response_model=Order)
async def create_order(order_data: OrderCreate):
    """Create a new order"""
    try:
        order = Order(**order_data.dict())
        order_dict = order.dict()
        
        # Store in database
        await orders_collection.insert_one(order_dict)
        
        # Send confirmation email
        await send_order_confirmation(order_dict)
        
        return order
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: str):
    """Get order by ID"""
    try:
        order = await orders_collection.find_one(
            {"id": order_id}, {"_id": 0}
        )
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Stripe Checkout endpoints
@api_router.post("/checkout/create-session")
async def create_checkout_session(request: Request, checkout_data: CheckoutRequest):
    """Create Stripe checkout session"""
    base_url = str(request.base_url)
    return await stripe_service.create_checkout_session(
        order_id=checkout_data.order_id,
        customer_email=checkout_data.customer_email,
        origin_url=checkout_data.origin_url
    )

@api_router.get("/checkout/status/{session_id}")
async def get_checkout_status(request: Request, session_id: str):
    """Get Stripe checkout session status"""
    base_url = str(request.base_url)
    return await stripe_service.get_checkout_status(session_id, base_url)

# Stripe webhook endpoint
@api_router.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    """Handle Stripe webhook events"""
    base_url = str(request.base_url)
    body = await request.body()
    stripe_signature = request.headers.get("Stripe-Signature")
    
    if not stripe_signature:
        raise HTTPException(status_code=400, detail="Missing Stripe signature")
    
    return await stripe_service.handle_webhook(body, stripe_signature, base_url)

# Custom orders endpoints
@api_router.post("/custom-orders", response_model=CustomOrder)
async def create_custom_order(custom_order_data: CustomOrderCreate):
    """Submit a custom t-shirt design order"""
    try:
        custom_order = CustomOrder(**custom_order_data.dict())
        custom_order_dict = custom_order.dict()
        
        # Store in database
        await custom_orders_collection.insert_one(custom_order_dict)
        
        # Send email notification
        await send_custom_order_notification(custom_order_dict)
        
        return custom_order
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/custom-orders", response_model=List[CustomOrder])
async def get_custom_orders():
    """Get all custom orders (admin endpoint)"""
    try:
        custom_orders = await custom_orders_collection.find({}, {"_id": 0}).to_list(1000)
        return custom_orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Newsletter endpoints
@api_router.post("/newsletter/subscribe", response_model=MessageResponse)
async def subscribe_newsletter(subscriber: NewsletterSubscribe):
    """Subscribe to newsletter"""
    try:
        # Check if email already exists
        existing = await newsletter_collection.find_one({"email": subscriber.email})
        if existing:
            raise HTTPException(status_code=400, detail="Email already subscribed")
        
        # Create new subscriber
        new_subscriber = NewsletterSubscriber(email=subscriber.email)
        await newsletter_collection.insert_one(new_subscriber.dict())
        
        return MessageResponse(message="Successfully subscribed to newsletter")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/newsletter/subscribers", response_model=List[NewsletterSubscriber])
async def get_newsletter_subscribers():
    """Get all newsletter subscribers (admin endpoint)"""
    try:
        subscribers = await newsletter_collection.find({}, {"_id": 0}).to_list(1000)
        return subscribers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Include the router in the main app
app.include_router(api_router)

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()