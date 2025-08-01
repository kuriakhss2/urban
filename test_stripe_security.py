#!/usr/bin/env python3
"""
Test script to verify Stripe Checkout security - amounts come from server-side orders
"""

import asyncio
import aiohttp
import json

# Get backend URL from frontend .env file
def get_backend_url():
    """Get backend URL from frontend environment"""
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    base_url = line.split('=', 1)[1].strip()
                    return f"{base_url}/api"
        return "http://localhost:8001/api"  # fallback
    except:
        return "http://localhost:8001/api"  # fallback

BASE_URL = get_backend_url()

async def test_stripe_security():
    """Test that Stripe checkout uses server-side order amounts, not frontend amounts"""
    print("🔍 Testing Stripe Checkout Security...")
    
    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        
        # Step 1: Create an order with a specific amount
        order_data = {
            "items": [
                {
                    "product_id": 1,
                    "name": "Urban Essential Tee",
                    "price": 28.0,
                    "quantity": 1,
                    "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop&crop=center"
                }
            ],
            "total": 28.0,  # Server-side amount
            "customer_email": "security.test@email.com"
        }
        
        # Create order
        async with session.post(f"{BASE_URL}/orders", json=order_data, 
                               headers={'Content-Type': 'application/json'}) as response:
            if response.status != 200:
                print(f"❌ Failed to create test order: {response.status}")
                return
            
            order = await response.json()
            order_id = order['id']
            print(f"✅ Created order {order_id} with amount: ${order['total']}")
        
        # Step 2: Create checkout session - the amount should come from server-side order
        checkout_data = {
            "order_id": order_id,
            "customer_email": "security.test@email.com",
            "origin_url": "https://example.com"
        }
        
        async with session.post(f"{BASE_URL}/checkout/create-session", json=checkout_data,
                               headers={'Content-Type': 'application/json'}) as response:
            if response.status != 200:
                print(f"❌ Failed to create checkout session: {response.status}")
                return
            
            checkout_session = await response.json()
            session_id = checkout_session['session_id']
            print(f"✅ Created checkout session: {session_id}")
        
        # Step 3: Verify the checkout session has the correct amount from server-side order
        async with session.get(f"{BASE_URL}/checkout/status/{session_id}") as response:
            if response.status != 200:
                print(f"❌ Failed to get checkout status: {response.status}")
                return
            
            status = await response.json()
            stripe_amount = status['amount_total']  # Stripe amounts are in cents
            expected_amount = int(28.0 * 100)  # Convert to cents
            
            print(f"Server-side order amount: $28.00")
            print(f"Stripe checkout amount: ${stripe_amount/100:.2f}")
            
            if stripe_amount == expected_amount:
                print("✅ SECURITY PASS: Stripe checkout uses server-side order amount")
            else:
                print(f"❌ SECURITY FAIL: Amount mismatch - expected ${expected_amount/100:.2f}, got ${stripe_amount/100:.2f}")
        
        # Step 4: Verify metadata contains order_id and customer_email
        metadata = status.get('metadata', {})
        if metadata.get('order_id') == order_id and metadata.get('customer_email') == "security.test@email.com":
            print("✅ SECURITY PASS: Metadata contains correct order_id and customer_email")
        else:
            print(f"❌ SECURITY FAIL: Metadata incorrect - {metadata}")

if __name__ == "__main__":
    asyncio.run(test_stripe_security())