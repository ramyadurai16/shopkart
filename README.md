# 🛒 ShopKart – Django E-Commerce Website

ShopKart is a dynamic and responsive e-commerce web application built using **Python, Django, and MySQL**.  
It provides a complete online shopping experience similar to popular platforms like Amazon and Flipkart.

---

## 🌐 Project Overview

ShopKart allows users to browse products by category, search for products, add items to cart, manage favourites, place orders, track order status, download invoices, and make online payments.  
The application is designed with a clean UI, user-friendly navigation, and scalable backend architecture.

---

## ✨ Features

- User Authentication (Register / Login / Logout)
- Category-based product listing
- Product search with category filter
- Product detail page with images
- Add to Cart & Remove from Cart
- Quantity-based price calculation
- Favourite / Wishlist functionality
- Order placement & order history
- Online payment integration (Razorpay / PhonePe)
- Order status tracking (Placed, Shipped, Out for Delivery, Delivered)
- Invoice generation & PDF download
- Cancel order option
- Admin panel for managing products, categories, and orders
- Responsive UI using Bootstrap

---

## 🖥️ Tech Stack

### Backend
- Python
- Django Framework

### Frontend
- HTML5
- CSS3
- Bootstrap
- JavaScript

### Database
- MySQL

### Payment Gateway
- Razorpay / PhonePe / Google Pay / Paytm

---

## 📸 Screenshots

### 🏠 Home Page & Collections
- Navbar with categories, search bar, cart, orders, and favourites
- Category listing with images

<p align="center">
  <img src="https://github.com/user-attachments/assets/d9405f96-bfd9-42de-bf24-b1eecfaf1841" width="800"/>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/8d30192e-5cff-4bb6-b090-cebb00cc431e" width="800"/>
</p>

---

### 📦 Orders Page
- Order history with payment status and total amount

<p align="center">
  <img src="https://github.com/user-attachments/assets/63057d12-92d4-4700-9fbb-501bac07622f" width="800"/>
</p>

---

### 📄 Order Details Page
- Order progress tracking
- Delivery address details
- Download invoice & cancel order option

<p align="center">
  <img src="https://github.com/user-attachments/assets/ffc4446a-4be9-41f1-b7e6-a59b41e902a3.png" width="800"/>
</p>

---

### 🧾 Invoice (PDF Download)
- Auto-generated tax invoice with order and customer details

<p align="center">
  <img src="https://github.com/user-attachments/assets/6170b633-6eb7-44be-92be-05c1c427d394.png" width="700"/>
</p>

---

### ❤️ Favourite / Wishlist Page
- View and remove favourite products

<p align="center">
  <img src="https://github.com/user-attachments/assets/edaffe2b-6c82-420a-b086-d97b7cf0cd2c.png" width="800"/>
</p>

---

### 🛒 Cart Page
- View cart items
- Quantity management
- Total amount calculation
- Checkout option

<p align="center">
  <img src="https://github.com/user-attachments/assets/0e415d31-b486-4074-b937-d60112c1ccdc.png" width="800"/>
</p>

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/ramyadurai16/shopkart-django-ecommerce.git
cd shopkart-django-ecommerce


### 2️⃣ Create Virtual Environment

python -m venv env
env\Scripts\activate

### 3️⃣ Install Dependencies
pip install -r requirements.txt

### 4️⃣ Configure Database

Create a MySQL database

Update database credentials in settings.py

### 5️⃣ Apply Migrations
python manage.py makemigrations
python manage.py migrate

### 6️⃣ Create Superuser
python manage.py createsuperuser

### 7️⃣ Run the Server
python manage.py runserver

- Open browser and visit:

http://127.0.0.1:8000/

## 🔐 Admin Panel

Access the admin panel at:

http://127.0.0.1:8000/admin/

### Admin Capabilities

- Add / update / delete products

- Manage categories

- View and manage orders

- Manage users

📁 Project Structure
shopkart/
├── shop/
├── cart/
├── orders/
├── templates/
├── static/
├── media/
├── manage.py

🚀 Future Enhancements

- Product reviews & ratings

- Coupon / discount system

- Email & SMS notifications

- Order return & refund system

- Cloud deployment (Render / PythonAnywhere)

📌 Project Purpose

- This project was developed for:

- Learning Django full-stack development

- Understanding real-world e-commerce workflows

- Academic, portfolio, and resume usage

🤝 Contribution

- Contributions are welcome.
- Feel free to fork this repository and submit a pull request.

📄 License

This project is created for educational purposes only.

👩‍💻 Author

RAMYA DM
GitHub: https://github.com/ramyadurai16

✅ GitHub Topics

django
python
ecommerce
mysql
bootstrap
web-development
django-ecommerce
razorpay-integration
full-stack

```
