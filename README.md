
---

# 📦 **E-Commerce API Documentation**

Beautifully documented REST API for products, carts, checkout, payments, analytics, and admin operations.

---

# 🔗 **Base URL**

```
http://127.0.0.1:8000
```

---

# 📘 **Authentication**

Some endpoints require authentication using **JWT tokens**:

```
Authorization: Bearer <your_token>
```

---

# 📚 **ENDPOINTS**

---

# 🛒 PRODUCT ENDPOINTS

---

## **1. Add Product**

### **POST** `/add_product/`

Create a new product (supports image upload).

### **Payload (multipart/form-data)**

| Field        | Type                         | Required | Description                   |
| ------------ | ---------------------------- | -------- | ----------------------------- |
| name         | string                       | ✔        | Product name                  |
| description  | string                       | ✔        | Product description           |
| category     | string                       | ✔        | Product category              |
| price        | decimal                      | ✔        | Product price                 |
| quantity     | integer                      | ✔        | Stock quantity                |
| minimumStock | integer                      | ✔        | Minimum stock alert threshold |
| featured     | boolean                      | ✖        | Whether product is featured   |
| image        | file (.jpg/.jpeg/.png, ≤5MB) | ✖        | Product image                 |

### **Sample Request**

```bash
POST /add_product/
Content-Type: multipart/form-data
```

### **Sample Response**

```json
{
  "id": 12,
  "name": "Nike Air Max",
  "category": "shoes",
  "description": "A stylish comfortable sneaker...",
  "price": "45.00",
  "quantity": 20,
  "minimumStock": 5,
  "featured": false,
  "sku": "SHO-93HD8A",
  "image": "http://localhost:8000/media/products/nike.jpg"
}
```

---

## **2. Generate Product Description (AI-Powered)**

### **POST** `/generate_product_description/`

Uses **Gemini AI** to generate a short product description.

### **Payload**

```json
{
  "name": "Wireless Bluetooth Headphones"
}
```

### **Sample Response**

```json
{
  "name": "Wireless Bluetooth Headphones",
  "description": "Experience crystal-clear audio..."
}
```

---

## **3. Get Paginated Products**

### **GET** `/get_products/`

### **Query Params**

| Param  | Description                        |
| ------ | ---------------------------------- |
| search | Filter by product name or category |
| page   | Page number                        |

### **Sample Response**

```json
{
  "count": 32,
  "next": "http://127.0.0.1:8000/api/get_products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 3,
      "name": "Samsung S24 Ultra",
      "price": "999.00",
      "category": "phones",
      "image": "...",
      "featured": true
    }
  ]
}
```

---

## **4. Get Single Product (By ID)**

### **GET** `/get_product/<pk>/`

### **Sample Response**

```json
{
  "id": 3,
  "name": "Samsung S24 Ultra",
  "price": "999.00",
  "category": "phones"
}
```

---

## **5. Get Product by Slug**

### **GET** `/get_product_by_slug/<slug>/`

---

## **6. Update Product**

### **PUT/PATCH** `/update_product/<pk>/`

### **Payload (any field optional)**

```json
{
  "name": "Updated Product",
  "price": "120.00",
  "featured": true
}
```

---

## **7. Delete Product**

### **DELETE** `/delete_product/<pk>/`

### **Sample Response**

```json
{
  "message": "Product 'Nike Air Max' has been successfully deleted."
}
```

---

## **8. Get Featured Products**

### **GET** `/get_featured_products/`

---

## **9. Get All Products + Search + Category Filter**

### **GET** `/get_all_products/`

### **Query Params**

| Param    | Example                 |
| -------- | ----------------------- |
| search   | "shoe"                  |
| category | "men" / "women" / "all" |
| page     | 1                       |

---

# 🛒 CART ENDPOINTS

---

## **1. Add to Cart**

### **POST** `/add_to_cart/`

### **Payload**

```json
{
  "cart_code": "abc123",
  "product_id": 5
}
```

---

## **2. Check if Product is in Cart**

### **GET** `/check_product_in_cart/`

### **Query Params**

| Param      | Required |
| ---------- | -------- |
| cart_code  | ✔        |
| product_id | ✔        |

### **Sample Response**

```json
{ "in_cart": true }
```

---

## **3. Increase Cart Item Quantity**

### **PUT** `/increase_cartitem_quantity/`

### **Payload**

```json
{ "item_id": 12 }
```

---

## **4. Decrease Cart Item Quantity**

### **PUT** `/decrease_cartitem_quantity/`

---

## **5. Delete Cart Item**

### **DELETE** `/delete_cartitem/<pk>/`

---

## **6. Get Cart**

### **GET** `/get_cart/<cart_code>/`

---

# 🧍‍♂️ SHIPPING & CHECKOUT

---

## **1. Create or Update Shipping Info**

### **POST** `/create_or_update_shipping_info/`

🔐 Requires Authentication

### **Payload**

```json
{
  "firstName": "Clinton",
  "lastName": "Nwachukwu",
  "email": "test@gmail.com",
  "address": "23 Lekki",
  "city": "Lagos",
  "state": "Lagos",
  "zipCode": "11001"
}
```

### **Response**

```json
{
  "message": "Shipping address updated successfully",
  "shipping_info": { ... }
}
```

---

# 💳 PAYMENT

---

## **1. Initialize Payment (Paystack)**

### **POST** `/initialize_payment/`

🔐 Requires Authentication

### **Payload**

```json
{
  "cart_code": "abc123"
}
```

### **Response**

```json
{
  "authorization_url": "https://checkout.paystack...",
  "access_code": "xyz123",
  "reference": "psk_9873sdf"
}
```

---

## **2. Verify Payment**

### **GET** `/verify_payment/<reference>/`

🔐 Requires Authentication

### **Response**

```json
{
  "message": "Payment verified successfully",
  "amount": 250.00,
  "currency": "NGN",
  "status": "success"
}
```

---

# 📦 ORDERS

---

## **1. Get User Orders**

### **GET** `/get_user_orders/`

🔐 Requires Authentication

---

## **2. Get All Orders (Admin)**

### **GET** `/get_all_orders/`

### **Query Params**

| Param  | Example                    |
| ------ | -------------------------- |
| status | success/pending/failed/all |
| sku    | "ORD-32SDF"                |
| page   | 1                          |

---

## **3. Update Order Status**

### **PUT** `/update_order_status/<pk>/`

### **Payload**

```json
{ "status": "success" }
```

---

## **4. Delete Order**

### **DELETE** `/delete_order/<pk>/`

📌 **Only pending orders older than 7 days can be deleted**

---

# 📊 ANALYTICS

---

## **Admin Analytics Dashboard**

### **GET** `/get_analytics_data/`

🔐 Requires Authentication

### **Sample Response**

```json
{
  "metrics": {
    "total_revenue": 2300.00,
    "total_orders": 43,
    "average_order_value": 53.48,
    "conversion_rate": 3.2
  },
  "sales_data": [...],
  "category_data": [...],
  "top_products": [...]
}
```

---

# 👥 USER STATUS

---

## **1. Check if User is Admin**

### **GET** `/user_is_admin/`

---

## **2. Check if User is Logged In**

### **GET** `/user_is_logged_in/`

### **Response**

```json
{
  "is_logged_in": true,
  "email": "test@gmail.com",
  "username": "clinton"
}
```

---

# 🔐 Authentication Endpoints

## **POST /auth/signup/**

Create a new user account.

### **Description**

Registers a new user using **email**, **username**, and **password**.
The email must be unique.

---

### **Request Body**

```json
{
  "email": "user@example.com",
  "username": "john_doe",
  "password": "yourpassword123"
}
```

---

### **Validation Rules**

| Field    | Required | Notes                                   |
| -------- | -------- | --------------------------------------- |
| email    | Yes      | Must be unique                          |
| username | No       | Optional in your current implementation |
| password | Yes      | Must not be empty                       |

---

### **Responses**

#### ✅ **201 Created**

```json
{
  "message": "User created successfully!",
  "user": {
    "email": "user@example.com",
    "username": "john_doe"
  }
}
```

#### ❌ **400 Bad Request – Missing fields**

```json
{
  "error": "Email and password are required."
}
```

#### ❌ **400 Bad Request – Email already exists**

```json
{
  "error": "User with this email already exists."
}
```

---

## **POST /auth/signin/**

Authenticate a user and return JWT tokens.

### **Description**

Logs in a user using **email** and **password**, then returns a **JWT refresh token** and **access token**.

---

### **Request Body**

```json
{
  "email": "user@example.com",
  "password": "yourpassword123"
}
```

---

### **Responses**

#### ✅ **200 OK**

```json
{
  "message": "Login successful.",
  "refresh": "jwt-refresh-token",
  "access": "jwt-access-token",
  "user": {
    "email": "user@example.com",
    "username": "john_doe"
  }
}
```

---

#### ❌ **400 Bad Request – Missing fields**

```json
{
  "error": "Email and password are required."
}
```

---

#### ❌ **404 Not Found – Email does not exist**

```json
{
  "error": "No account found with this email."
}
```

---

#### ❌ **401 Unauthorized – Wrong password**

```json
{
  "error": "Incorrect password."
}
```

---
