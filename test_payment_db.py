#!/usr/bin/env python3
"""
Test script to verify payment_transactions collection is working
"""

import asyncio
import aiohttp
import json
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
ROOT_DIR = Path(__file__).parent / 'backend'
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

async def test_payment_transactions_collection():
    """Test if payment_transactions collection exists and has data"""
    print("🔍 Testing payment_transactions collection...")
    
    try:
        # Check if collection exists and has documents
        count = await db.payment_transactions.count_documents({})
        print(f"Payment transactions count: {count}")
        
        if count > 0:
            # Get the latest payment transaction
            latest_transaction = await db.payment_transactions.find_one(
                {}, sort=[("created_at", -1)]
            )
            print(f"Latest payment transaction: {latest_transaction}")
            
            # Verify required fields
            required_fields = ['id', 'session_id', 'amount', 'currency', 'payment_status', 'status', 'metadata']
            missing_fields = [field for field in required_fields if field not in latest_transaction]
            
            if not missing_fields:
                print("✅ Payment transaction has all required fields")
            else:
                print(f"❌ Missing fields in payment transaction: {missing_fields}")
        else:
            print("⚠️ No payment transactions found in database")
            
    except Exception as e:
        print(f"❌ Error accessing payment_transactions collection: {str(e)}")
    
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(test_payment_transactions_collection())