# URBAN THREADS - API Contracts & Integration Guide

## API Contracts

### Products API
- `GET /api/products` - Get all products
- `GET /api/products/category/{category}` - Get products by category (clothes, socks, books, shoes)

### Orders API
- `POST /api/orders` - Create new order from cart
- `GET /api/orders/{order_id}` - Get order details

### Custom Orders API
- `POST /api/custom-orders` - Submit custom t-shirt design order
- `GET /api/custom-orders` - Get all custom orders (admin)

### Newsletter API
- `POST /api/newsletter/subscribe` - Subscribe to newsletter
- `GET /api/newsletter/subscribers` - Get all subscribers (admin)

## Mock Data Replacement

### Frontend Mock Data (mock.js) to Replace:
1. **mockProducts** array → Replace with API calls to `/api/products`
2. **mockCustomOrders** array → Replace with API calls to `/api/custom-orders`  
3. **mockNewsletterSubscribers** array → Replace with API calls to `/api/newsletter/subscribe`

### Cart Functionality:
- Currently stored in React context (frontend only)
- Add checkout API to process cart items into orders
- Keep cart in frontend context but add backend order processing

## Backend Implementation Plan

### Database Models:
1. **Product Model**: id, name, category, price, image, description
2. **Order Model**: id, items[], total, customer_email, status, created_at
3. **CustomOrder Model**: id, email, custom_text, description, file_name, status, created_at
4. **NewsletterSubscriber Model**: id, email, subscribed_at

### Email Integration:
- Send email notifications for custom orders
- Store custom order requests in database
- Provide admin endpoint to view custom orders

## Frontend Integration Changes

### Files to Update:
1. **mock.js** - Remove mock arrays, keep as empty arrays initially
2. **pages/Home.js** - Replace mockProducts with API call
3. **pages/ProductCategory.js** - Replace categoryProducts filter with API call
4. **pages/Cart.js** - Add checkout API call on order submission
5. **pages/CustomDesign.js** - Replace mock storage with API call
6. **components/Footer.js** - Replace mock newsletter with API call

### API Integration Pattern:
```javascript
// Replace mock data usage like this:
const [products, setProducts] = useState([]);

useEffect(() => {
  const fetchProducts = async () => {
    const response = await axios.get(`${API}/products`);
    setProducts(response.data);
  };
  fetchProducts();
}, []);
```

## Environment Variables Needed:
- EMAIL_SERVICE_API_KEY (for sending custom order notifications)
- ADMIN_EMAIL (to receive custom order notifications)

## Testing Protocol:
1. Test all product CRUD operations
2. Test cart checkout flow with order creation
3. Test custom order submission and email sending
4. Test newsletter subscription
5. Verify all frontend mock data is replaced with API calls