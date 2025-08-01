#!/usr/bin/env python3
"""
Urban Threads Backend API Test Suite
Tests all backend endpoints comprehensively
"""

import asyncio
import aiohttp
import json
import os
from datetime import datetime
from typing import Dict, List, Any

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

class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
        
    def log_pass(self, test_name: str):
        print(f"✅ PASS: {test_name}")
        self.passed += 1
        
    def log_fail(self, test_name: str, error: str):
        print(f"❌ FAIL: {test_name} - {error}")
        self.failed += 1
        self.errors.append(f"{test_name}: {error}")
        
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"TEST SUMMARY")
        print(f"{'='*60}")
        print(f"Total Tests: {total}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Success Rate: {(self.passed/total*100):.1f}%" if total > 0 else "No tests run")
        
        if self.errors:
            print(f"\nFAILED TESTS:")
            for error in self.errors:
                print(f"  - {error}")

results = TestResults()

async def make_request(session: aiohttp.ClientSession, method: str, url: str, 
                      data: Dict = None, expected_status: int = 200) -> Dict:
    """Make HTTP request and return response"""
    try:
        if method.upper() == 'GET':
            async with session.get(url) as response:
                response_data = await response.json()
                return {
                    'status': response.status,
                    'data': response_data,
                    'success': response.status == expected_status
                }
        elif method.upper() == 'POST':
            headers = {'Content-Type': 'application/json'}
            async with session.post(url, json=data, headers=headers) as response:
                response_data = await response.json()
                return {
                    'status': response.status,
                    'data': response_data,
                    'success': response.status == expected_status
                }
    except Exception as e:
        return {
            'status': 0,
            'data': None,
            'success': False,
            'error': str(e)
        }

async def test_health_check(session: aiohttp.ClientSession):
    """Test API health check"""
    print(f"\n🔍 Testing Health Check...")
    
    response = await make_request(session, 'GET', f"{BASE_URL}/")
    
    if response['success'] and response['data'].get('message'):
        results.log_pass("Health Check - API is running")
    else:
        results.log_fail("Health Check", f"Status: {response['status']}, Data: {response.get('data')}")

async def test_products_api(session: aiohttp.ClientSession):
    """Test Products API endpoints"""
    print(f"\n🔍 Testing Products API...")
    
    # Test 1: Get all products (should return 20 products)
    response = await make_request(session, 'GET', f"{BASE_URL}/products")
    
    if response['success']:
        products = response['data']
        if isinstance(products, list) and len(products) == 20:
            results.log_pass("GET /products - Returns 20 products")
        else:
            results.log_fail("GET /products", f"Expected 20 products, got {len(products) if isinstance(products, list) else 'non-list'}")
    else:
        results.log_fail("GET /products", f"Status: {response['status']}")
    
    # Test 2: Get products by category - clothes
    response = await make_request(session, 'GET', f"{BASE_URL}/products/category/clothes")
    
    if response['success']:
        clothes = response['data']
        if isinstance(clothes, list) and len(clothes) == 5:
            # Verify all products are clothes category
            all_clothes = all(product.get('category') == 'clothes' for product in clothes)
            if all_clothes:
                results.log_pass("GET /products/category/clothes - Returns 5 clothes products")
            else:
                results.log_fail("GET /products/category/clothes", "Some products are not clothes category")
        else:
            results.log_fail("GET /products/category/clothes", f"Expected 5 clothes, got {len(clothes) if isinstance(clothes, list) else 'non-list'}")
    else:
        results.log_fail("GET /products/category/clothes", f"Status: {response['status']}")
    
    # Test 3: Get products by category - socks
    response = await make_request(session, 'GET', f"{BASE_URL}/products/category/socks")
    
    if response['success']:
        socks = response['data']
        if isinstance(socks, list) and len(socks) == 5:
            all_socks = all(product.get('category') == 'socks' for product in socks)
            if all_socks:
                results.log_pass("GET /products/category/socks - Returns 5 socks products")
            else:
                results.log_fail("GET /products/category/socks", "Some products are not socks category")
        else:
            results.log_fail("GET /products/category/socks", f"Expected 5 socks, got {len(socks) if isinstance(socks, list) else 'non-list'}")
    else:
        results.log_fail("GET /products/category/socks", f"Status: {response['status']}")
    
    # Test 4: Get products by category - books
    response = await make_request(session, 'GET', f"{BASE_URL}/products/category/books")
    
    if response['success']:
        books = response['data']
        if isinstance(books, list) and len(books) == 5:
            all_books = all(product.get('category') == 'books' for product in books)
            if all_books:
                results.log_pass("GET /products/category/books - Returns 5 books products")
            else:
                results.log_fail("GET /products/category/books", "Some products are not books category")
        else:
            results.log_fail("GET /products/category/books", f"Expected 5 books, got {len(books) if isinstance(books, list) else 'non-list'}")
    else:
        results.log_fail("GET /products/category/books", f"Status: {response['status']}")
    
    # Test 5: Get products by category - shoes
    response = await make_request(session, 'GET', f"{BASE_URL}/products/category/shoes")
    
    if response['success']:
        shoes = response['data']
        if isinstance(shoes, list) and len(shoes) == 5:
            all_shoes = all(product.get('category') == 'shoes' for product in shoes)
            if all_shoes:
                results.log_pass("GET /products/category/shoes - Returns 5 shoes products")
            else:
                results.log_fail("GET /products/category/shoes", "Some products are not shoes category")
        else:
            results.log_fail("GET /products/category/shoes", f"Expected 5 shoes, got {len(shoes) if isinstance(shoes, list) else 'non-list'}")
    else:
        results.log_fail("GET /products/category/shoes", f"Status: {response['status']}")
    
    # Test 6: Get single product by ID
    response = await make_request(session, 'GET', f"{BASE_URL}/products/1")
    
    if response['success']:
        product = response['data']
        if isinstance(product, dict) and product.get('id') == 1:
            expected_fields = ['id', 'category', 'name', 'price', 'image', 'description']
            has_all_fields = all(field in product for field in expected_fields)
            if has_all_fields:
                results.log_pass("GET /products/1 - Returns single product with all fields")
            else:
                missing_fields = [field for field in expected_fields if field not in product]
                results.log_fail("GET /products/1", f"Missing fields: {missing_fields}")
        else:
            results.log_fail("GET /products/1", f"Invalid product data: {product}")
    else:
        results.log_fail("GET /products/1", f"Status: {response['status']}")
    
    # Test 7: Get non-existent product (should return 404)
    response = await make_request(session, 'GET', f"{BASE_URL}/products/999", expected_status=404)
    
    if response['success']:
        results.log_pass("GET /products/999 - Returns 404 for non-existent product")
    else:
        results.log_fail("GET /products/999", f"Expected 404, got {response['status']}")

async def test_orders_api(session: aiohttp.ClientSession):
    """Test Orders API endpoints"""
    print(f"\n🔍 Testing Orders API...")
    
    # Test 1: Create a new order
    order_data = {
        "items": [
            {
                "product_id": 1,
                "name": "Urban Essential Tee",
                "price": 28.0,
                "quantity": 2,
                "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop&crop=center"
            },
            {
                "product_id": 6,
                "name": "Comfort Crew Socks",
                "price": 20.0,
                "quantity": 1,
                "image": "https://images.unsplash.com/photo-1586350977771-b3b0abd50c82?w=400&h=400&fit=crop&crop=center"
            }
        ],
        "total": 76.0,
        "customer_email": "sarah.johnson@email.com"
    }
    
    response = await make_request(session, 'POST', f"{BASE_URL}/orders", data=order_data)
    
    order_id = None
    if response['success']:
        order = response['data']
        if isinstance(order, dict) and 'id' in order:
            order_id = order['id']
            expected_fields = ['id', 'items', 'total', 'customer_email', 'status', 'created_at']
            has_all_fields = all(field in order for field in expected_fields)
            if has_all_fields and order['total'] == 76.0:
                results.log_pass("POST /orders - Creates order successfully")
            else:
                results.log_fail("POST /orders", f"Missing fields or incorrect total: {order}")
        else:
            results.log_fail("POST /orders", f"Invalid order response: {order}")
    else:
        results.log_fail("POST /orders", f"Status: {response['status']}, Data: {response.get('data')}")
    
    # Test 2: Get order by ID (if order was created successfully)
    if order_id:
        response = await make_request(session, 'GET', f"{BASE_URL}/orders/{order_id}")
        
        if response['success']:
            retrieved_order = response['data']
            if isinstance(retrieved_order, dict) and retrieved_order.get('id') == order_id:
                results.log_pass("GET /orders/{order_id} - Retrieves order successfully")
            else:
                results.log_fail("GET /orders/{order_id}", f"Order ID mismatch: {retrieved_order}")
        else:
            results.log_fail("GET /orders/{order_id}", f"Status: {response['status']}")
    
    # Test 3: Get non-existent order (should return 404)
    response = await make_request(session, 'GET', f"{BASE_URL}/orders/non-existent-id", expected_status=404)
    
    if response['success']:
        results.log_pass("GET /orders/non-existent-id - Returns 404 for non-existent order")
    else:
        results.log_fail("GET /orders/non-existent-id", f"Expected 404, got {response['status']}")

async def test_custom_orders_api(session: aiohttp.ClientSession):
    """Test Custom Orders API endpoints"""
    print(f"\n🔍 Testing Custom Orders API...")
    
    # Test 1: Create a custom order
    custom_order_data = {
        "email": "alex.designer@email.com",
        "custom_text": "URBAN VIBES",
        "description": "I want a minimalist design with 'URBAN VIBES' text in a modern font on a black t-shirt. The text should be centered and in white color."
    }
    
    response = await make_request(session, 'POST', f"{BASE_URL}/custom-orders", data=custom_order_data)
    
    if response['success']:
        custom_order = response['data']
        if isinstance(custom_order, dict) and 'id' in custom_order:
            expected_fields = ['id', 'email', 'custom_text', 'description', 'status', 'created_at']
            has_all_fields = all(field in custom_order for field in expected_fields)
            if has_all_fields and custom_order['email'] == "alex.designer@email.com":
                results.log_pass("POST /custom-orders - Creates custom order successfully")
            else:
                results.log_fail("POST /custom-orders", f"Missing fields or incorrect data: {custom_order}")
        else:
            results.log_fail("POST /custom-orders", f"Invalid custom order response: {custom_order}")
    else:
        results.log_fail("POST /custom-orders", f"Status: {response['status']}, Data: {response.get('data')}")
    
    # Test 2: Create another custom order with different data
    custom_order_data2 = {
        "email": "maria.creative@email.com",
        "custom_text": "BE YOURSELF",
        "description": "Looking for a vintage-style design with 'BE YOURSELF' in retro typography on a cream-colored shirt."
    }
    
    response = await make_request(session, 'POST', f"{BASE_URL}/custom-orders", data=custom_order_data2)
    
    if response['success']:
        results.log_pass("POST /custom-orders - Creates second custom order successfully")
    else:
        results.log_fail("POST /custom-orders (second)", f"Status: {response['status']}")
    
    # Test 3: Get all custom orders
    response = await make_request(session, 'GET', f"{BASE_URL}/custom-orders")
    
    if response['success']:
        custom_orders = response['data']
        if isinstance(custom_orders, list) and len(custom_orders) >= 2:
            # Check if our test orders are in the list
            emails = [order.get('email') for order in custom_orders]
            if "alex.designer@email.com" in emails and "maria.creative@email.com" in emails:
                results.log_pass("GET /custom-orders - Returns all custom orders including test orders")
            else:
                results.log_fail("GET /custom-orders", f"Test orders not found in response: {emails}")
        else:
            results.log_fail("GET /custom-orders", f"Expected at least 2 orders, got {len(custom_orders) if isinstance(custom_orders, list) else 'non-list'}")
    else:
        results.log_fail("GET /custom-orders", f"Status: {response['status']}")

async def test_newsletter_api(session: aiohttp.ClientSession):
    """Test Newsletter API endpoints"""
    print(f"\n🔍 Testing Newsletter API...")
    
    # Test 1: Subscribe to newsletter
    subscriber_data = {
        "email": "newsletter.subscriber@email.com"
    }
    
    response = await make_request(session, 'POST', f"{BASE_URL}/newsletter/subscribe", data=subscriber_data)
    
    if response['success']:
        result = response['data']
        if isinstance(result, dict) and result.get('message') == "Successfully subscribed to newsletter":
            results.log_pass("POST /newsletter/subscribe - Subscribes successfully")
        else:
            results.log_fail("POST /newsletter/subscribe", f"Unexpected response: {result}")
    else:
        results.log_fail("POST /newsletter/subscribe", f"Status: {response['status']}, Data: {response.get('data')}")
    
    # Test 2: Try to subscribe with same email (should fail with 400)
    response = await make_request(session, 'POST', f"{BASE_URL}/newsletter/subscribe", 
                                data=subscriber_data, expected_status=400)
    
    if response['success']:
        result = response['data']
        if isinstance(result, dict) and "already subscribed" in result.get('detail', '').lower():
            results.log_pass("POST /newsletter/subscribe - Prevents duplicate subscription")
        else:
            results.log_fail("POST /newsletter/subscribe (duplicate)", f"Unexpected error message: {result}")
    else:
        results.log_fail("POST /newsletter/subscribe (duplicate)", f"Expected 400, got {response['status']}")
    
    # Test 3: Subscribe another email
    subscriber_data2 = {
        "email": "another.subscriber@email.com"
    }
    
    response = await make_request(session, 'POST', f"{BASE_URL}/newsletter/subscribe", data=subscriber_data2)
    
    if response['success']:
        results.log_pass("POST /newsletter/subscribe - Subscribes second email successfully")
    else:
        results.log_fail("POST /newsletter/subscribe (second)", f"Status: {response['status']}")
    
    # Test 4: Get all newsletter subscribers
    response = await make_request(session, 'GET', f"{BASE_URL}/newsletter/subscribers")
    
    if response['success']:
        subscribers = response['data']
        if isinstance(subscribers, list) and len(subscribers) >= 2:
            # Check if our test subscribers are in the list
            emails = [sub.get('email') for sub in subscribers]
            if "newsletter.subscriber@email.com" in emails and "another.subscriber@email.com" in emails:
                results.log_pass("GET /newsletter/subscribers - Returns all subscribers including test subscribers")
            else:
                results.log_fail("GET /newsletter/subscribers", f"Test subscribers not found: {emails}")
        else:
            results.log_fail("GET /newsletter/subscribers", f"Expected at least 2 subscribers, got {len(subscribers) if isinstance(subscribers, list) else 'non-list'}")
    else:
        results.log_fail("GET /newsletter/subscribers", f"Status: {response['status']}")

async def test_error_handling(session: aiohttp.ClientSession):
    """Test error handling scenarios"""
    print(f"\n🔍 Testing Error Handling...")
    
    # Test 1: Invalid order data (missing required fields)
    invalid_order = {
        "items": [],  # Empty items
        "total": 0
        # Missing customer_email
    }
    
    response = await make_request(session, 'POST', f"{BASE_URL}/orders", 
                                data=invalid_order, expected_status=422)
    
    if response['success']:
        results.log_pass("POST /orders with invalid data - Returns 422 validation error")
    else:
        results.log_fail("POST /orders with invalid data", f"Expected 422, got {response['status']}")
    
    # Test 2: Invalid custom order data (missing email)
    invalid_custom_order = {
        "custom_text": "TEST",
        "description": "Test description"
        # Missing email
    }
    
    response = await make_request(session, 'POST', f"{BASE_URL}/custom-orders", 
                                data=invalid_custom_order, expected_status=422)
    
    if response['success']:
        results.log_pass("POST /custom-orders with invalid data - Returns 422 validation error")
    else:
        results.log_fail("POST /custom-orders with invalid data", f"Expected 422, got {response['status']}")
    
    # Test 3: Invalid newsletter subscription (missing email)
    invalid_subscription = {}
    
    response = await make_request(session, 'POST', f"{BASE_URL}/newsletter/subscribe", 
                                data=invalid_subscription, expected_status=422)
    
    if response['success']:
        results.log_pass("POST /newsletter/subscribe with invalid data - Returns 422 validation error")
    else:
        results.log_fail("POST /newsletter/subscribe with invalid data", f"Expected 422, got {response['status']}")

async def run_all_tests():
    """Run all backend API tests"""
    print(f"🚀 Starting Urban Threads Backend API Tests")
    print(f"Backend URL: {BASE_URL}")
    print(f"{'='*60}")
    
    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            # Run all test suites
            await test_health_check(session)
            await test_products_api(session)
            await test_orders_api(session)
            await test_custom_orders_api(session)
            await test_newsletter_api(session)
            await test_error_handling(session)
            
        except Exception as e:
            print(f"❌ Test execution error: {str(e)}")
            results.log_fail("Test Execution", str(e))
    
    # Print final results
    results.summary()
    
    # Return success status
    return results.failed == 0

if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    exit(0 if success else 1)