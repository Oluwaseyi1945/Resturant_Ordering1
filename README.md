# Restaurant Ordering API

A RESTful restaurant ordering API built with **Django** and **Django REST Framework**. The API allows customers to browse available menu items, create and manage orders, and track order status.

JWT authentication is used to secure customer and staff operations.

## 🚀 Features

* View available restaurant menu items
* Create customer orders
* View a customer's orders
* View individual order details
* Add items to pending orders
* Remove items from pending orders
* Update order status for staff users
* JWT authentication
* Django Admin support
* SQLite database for development

## 🛠️ Technologies

* Python
* Django 6.0.7
* Django REST Framework
* Simple JWT
* SQLite
* Git & GitHub

## 📁 Project Structure

```text
Resturant_Ordering1/
│
├── orders/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── restaurant_api/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── .gitignore
├── manage.py
└── README.md
```
## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Oluwaseyi1945/Resturant_Ordering1.git
```

### 2. Navigate into the project

```bash
cd Resturant_Ordering1
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Apply migrations

```bash
python manage.py migrate
```

### 7. Create a superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 8. Start the development server

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```


## 🔐 Authentication

The API uses **JWT (JSON Web Token)** authentication.

### Obtain a token

**POST**

```text
/api/token/
```

Example request:

```json
{
    "username": "your_username",
    "password": "your_password"
}
```

Example response:

```json
{
    "refresh": "your_refresh_token",
    "access": "your_access_token"
}
```

Use the access token when making authenticated requests.

### Authorization Header

```text
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Refresh Token

**POST**

```text
/api/token/refresh/
```

Example:

```json
{
    "refresh": "YOUR_REFRESH_TOKEN"
}
```

## 🍽️ API Endpoints

### 1. Get Available Menu Items

**GET**

```text
/api/menuitem/
```

This endpoint is publicly accessible and returns available menu items.

Example:

```bash
curl http://127.0.0.1:8000/api/menuitem/
```

---

### 2. Get Customer Orders

**GET**

```text
/api/orders/
```

Authentication required.

```text
Authorization: Bearer YOUR_ACCESS_TOKEN
```

Returns the orders belonging to the authenticated customer.

---

### 3. Create an Order

**POST**

```text
/api/orders/
```

Authentication required.

Example request:

```json
{
    "items": [
        {
            "menu_item": 1,
            "quantity": 2
        },
        {
            "menu_item": 2,
            "quantity": 1
        }
    ]
}
```

Each order must contain at least one menu item.

---

### 4. Get Order Details

**GET**

```text
/api/orders/<id>/
```

Example:

```text
/api/orders/1/
```

Authentication required.

Customers can only view their own orders.

---

### 5. Add an Item to an Order

**PATCH**

```text
/api/orders/<id>/add-item/
```

Authentication required.

Example:

```json
{
    "menu_item": 3,
    "quantity": 2
}
```

Only orders with a `pending` status can be modified.

---

### 6. Remove an Item from an Order

**DELETE**

```text
/api/orders/<id>/items/<item_id>/
```

Authentication required.

Example:

```text
/api/orders/1/items/2/
```

Only items belonging to the specified order can be removed.

---

### 7. Update Order Status

**PATCH**

```text
/api/orders/<id>/status/
```

Authentication required.

Only staff users can update order status.

Example:

```json
{
    "status": "preparing"
}
```

### Order Status Flow

```text
pending
   ↓
preparing
   ↓
ready
   ↓
completed
```

A pending order can also be cancelled:

```text
pending → cancelled
```

Invalid status transitions are rejected by the API.

## 🧪 Testing

Run Django's system checks:

```bash
python manage.py check
```

Run the test suite:

```bash
python manage.py test orders
```

## 🔧 Django Admin

The Django Admin interface can be accessed at:

```text
http://127.0.0.1:8000/admin/
```

Log in using the superuser account created during installation.

## 📌 API Testing

You can test the API using tools such as:

* Thunder Client
* Postman
* cURL
* Insomnia

A typical testing flow is:

```text
1. Create a user
2. Obtain JWT access token
3. Get available menu items
4. Create an order
5. View the order
6. Add/remove order items
7. Update order status as a staff user
```

## 🔒 Security

This project uses JWT authentication for protected API endpoints.

Do not commit sensitive information such as:

* Secret keys
* Passwords
* API keys
* Production credentials
* Environment variables containing secrets

For production deployment, sensitive configuration should be stored in environment variables.

## 📚 What I Learned

This project demonstrates practical experience with:

* Django REST Framework
* REST API development
* APIView-based endpoints
* Serializers
* Django models and relationships
* JWT authentication
* Permissions
* CRUD operations
* HTTP methods such as GET, POST, PATCH and DELETE
* Order workflow management
* API testing
* Git and GitHub

## 👨‍💻 Author

**Oluwaseyi Oladejo**

Python / Django Developer

GitHub:
https://github.com/Oluwaseyi1945

## 📄 License

This project is intended for learning and portfolio purposes.
