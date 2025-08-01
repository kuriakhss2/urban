from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Collections
products_collection = db.products
orders_collection = db.orders
custom_orders_collection = db.custom_orders
newsletter_collection = db.newsletter_subscribers

async def init_products():
    """Initialize products in database if they don't exist"""
    existing_count = await products_collection.count_documents({})
    
    if existing_count == 0:
        initial_products = [
            # Clothes
            {
                "id": 1,
                "category": "clothes",
                "name": "Urban Essential Tee",
                "price": 28,
                "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop&crop=center",
                "description": "Comfortable cotton blend t-shirt perfect for everyday wear"
            },
            {
                "id": 2,
                "category": "clothes",
                "name": "Minimalist Hoodie",
                "price": 45,
                "image": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400&h=400&fit=crop&crop=center",
                "description": "Premium quality hoodie with modern cut and feel"
            },
            {
                "id": 3,
                "category": "clothes",
                "name": "Street Style Jacket",
                "price": 50,
                "image": "https://images.unsplash.com/photo-1544022613-e87ca75a784a?w=400&h=400&fit=crop&crop=center",
                "description": "Versatile jacket that pairs with any outfit"
            },
            {
                "id": 4,
                "category": "clothes",
                "name": "Classic Joggers",
                "price": 35,
                "image": "https://images.unsplash.com/photo-1506629905607-d9b0b5a6f2f5?w=400&h=400&fit=crop&crop=center",
                "description": "Comfortable joggers for casual and athletic wear"
            },
            {
                "id": 5,
                "category": "clothes",
                "name": "Urban Tank Top",
                "price": 22,
                "image": "https://images.unsplash.com/photo-1503341338985-b019968ba004?w=400&h=400&fit=crop&crop=center",
                "description": "Lightweight tank perfect for summer days"
            },
            
            # Socks
            {
                "id": 6,
                "category": "socks",
                "name": "Comfort Crew Socks",
                "price": 20,
                "image": "https://images.unsplash.com/photo-1586350977771-b3b0abd50c82?w=400&h=400&fit=crop&crop=center",
                "description": "Ultra-soft crew socks for all-day comfort"
            },
            {
                "id": 7,
                "category": "socks",
                "name": "Athletic Performance Socks",
                "price": 25,
                "image": "https://images.unsplash.com/photo-1544966503-7cc5ac882d5f?w=400&h=400&fit=crop&crop=center",
                "description": "Moisture-wicking socks for active lifestyles"
            },
            {
                "id": 8,
                "category": "socks",
                "name": "Minimalist Ankle Socks",
                "price": 18,
                "image": "https://images.unsplash.com/photo-1559709120-6867ecc1f9b6?w=400&h=400&fit=crop&crop=center",
                "description": "Low-profile ankle socks with clean design"
            },
            {
                "id": 9,
                "category": "socks",
                "name": "Cozy Wool Blend Socks",
                "price": 30,
                "image": "https://images.unsplash.com/photo-1584464491033-06628f3a6b7b?w=400&h=400&fit=crop&crop=center",
                "description": "Warm and comfortable wool blend for cold days"
            },
            {
                "id": 10,
                "category": "socks",
                "name": "Pattern Play Socks",
                "price": 23,
                "image": "https://images.unsplash.com/photo-1505022610485-0249ba5b3675?w=400&h=400&fit=crop&crop=center",
                "description": "Stylish patterned socks to add flair to any outfit"
            },

            # Books
            {
                "id": 11,
                "category": "books",
                "name": "Urban Style Guide",
                "price": 32,
                "image": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&h=400&fit=crop&crop=center",
                "description": "Complete guide to modern urban fashion and lifestyle"
            },
            {
                "id": 12,
                "category": "books",
                "name": "Street Photography Collection",
                "price": 40,
                "image": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400&h=400&fit=crop&crop=center",
                "description": "Inspiring collection of urban street photography"
            },
            {
                "id": 13,
                "category": "books",
                "name": "Minimalist Living",
                "price": 26,
                "image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop&crop=center",
                "description": "Guide to simplified, intentional living"
            },
            {
                "id": 14,
                "category": "books",
                "name": "Creative Inspiration",
                "price": 35,
                "image": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400&h=400&fit=crop&crop=center",
                "description": "Fuel your creative journey with this inspiring read"
            },
            {
                "id": 15,
                "category": "books",
                "name": "Urban Culture Journal",
                "price": 24,
                "image": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400&h=400&fit=crop&crop=center",
                "description": "Explore the pulse of city culture and trends"
            },

            # Shoes
            {
                "id": 16,
                "category": "shoes",
                "name": "Urban Sneakers",
                "price": 48,
                "image": "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400&h=400&fit=crop&crop=center",
                "description": "Versatile sneakers for city adventures"
            },
            {
                "id": 17,
                "category": "shoes",
                "name": "Minimalist Loafers",
                "price": 42,
                "image": "https://images.unsplash.com/photo-1584634644929-c4aa3d4af4e2?w=400&h=400&fit=crop&crop=center",
                "description": "Clean, comfortable loafers for professional wear"
            },
            {
                "id": 18,
                "category": "shoes",
                "name": "Street Style Boots",
                "price": 50,
                "image": "https://images.unsplash.com/photo-1605348532760-6753d2c43329?w=400&h=400&fit=crop&crop=center",
                "description": "Durable boots with urban aesthetic"
            },
            {
                "id": 19,
                "category": "shoes",
                "name": "Athletic Runners",
                "price": 45,
                "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop&crop=center",
                "description": "Performance running shoes for active lifestyles"
            },
            {
                "id": 20,
                "category": "shoes",  
                "name": "Canvas Casuals",
                "price": 35,
                "image": "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=400&h=400&fit=crop&crop=center",
                "description": "Comfortable canvas shoes for everyday wear"
            }
        ]
        
        await products_collection.insert_many(initial_products)
        print(f"Initialized {len(initial_products)} products in database")