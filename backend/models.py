from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime
import uuid

# Product Models
class Product(BaseModel):
    id: int
    category: str
    name: str
    price: float
    image: str
    description: str

class ProductCreate(BaseModel):
    category: str
    name: str
    price: float
    image: str
    description: str

# Order Models
class OrderItem(BaseModel):
    product_id: int
    name: str
    price: float
    quantity: int
    image: str

class Order(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    items: List[OrderItem]
    total: float
    customer_email: EmailStr
    status: str = "pending"
    created_at: datetime = Field(default_factory=datetime.utcnow)

class OrderCreate(BaseModel):
    items: List[OrderItem]
    total: float
    customer_email: EmailStr

# Custom Order Models
class CustomOrder(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    custom_text: Optional[str] = None
    description: Optional[str] = None
    file_name: Optional[str] = None
    status: str = "pending"
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CustomOrderCreate(BaseModel):
    email: EmailStr
    custom_text: Optional[str] = None
    description: Optional[str] = None
    file_name: Optional[str] = None

# Newsletter Models
class NewsletterSubscriber(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    subscribed_at: datetime = Field(default_factory=datetime.utcnow)

class NewsletterSubscribe(BaseModel):
    email: EmailStr

# Response Models
class MessageResponse(BaseModel):
    message: str