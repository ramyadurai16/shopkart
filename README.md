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

<p align="center">
  <img src="https://github.com/user-attachments/assets/a37e9d5f-b11a-46b0-b310-dbd2eef07abb" width="800"/>
</p>

---

### 📦 Orders Page
- Order history with payment status and total amount

<p align="center">
  <img src="https://github.com/user-attachments/assets/e35817bf-cc9c-480d-a5aa-7bea20652c4a" width="800"/>
</p>

---

### 📄 Order Details Page
- Order progress tracking
- Delivery address details
- Download invoice & cancel order option

<p align="center">
  <img src="https://github.com/user-attachments/assets/74cdbee0-494b-4115-82d1-a386e36bf147" width="800"/>
</p>

---

### 🧾 Invoice (PDF Download)
- Auto-generated tax invoice with order and customer details

<p align="center">
  <img src="https://github.com/user-attachments/assets/223ec23c-1ae1-4a73-b473-ab49c8a92b3e" width="700"/>
</p>

---

### ❤️ Favourite / Wishlist Page
- View and remove favourite products

<p align="center">
  <img src="https://github.com/user-attachments/assets/276580f6-5a5c-4f98-83a6-e3ca4eea63a2" width="800"/>
</p>

---

### 🛒 Cart Page
- View cart items
- Quantity management
- Total amount calculation
- Checkout option

<p align="center">
  <img src="https://github.com/user-attachments/assets/c3e39484-1bd2-4554-a4d0-33e952c92302" width="800"/>
</p>

---

## ⚙️ Installation & Setup

```bash
1️⃣ Clone the Repository

git clone https://github.com/ramyadurai16/shopkart-django-ecommerce.git
cd shopkart-django-ecommerce


2️⃣ Create Virtual Environment

python -m venv env
env\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Configure Database

Create a MySQL database

Update database credentials in settings.py

5️⃣ Apply Migrations
python manage.py makemigrations
python manage.py migrate

6️⃣ Create Superuser
python manage.py createsuperuser

7️⃣ Run the Server
python manage.py runserver

- Open browser and visit:

http://127.0.0.1:8000/
```
---

## 🔐 Admin Panel

Access the admin panel at:

http://127.0.0.1:8000/admin/

### Admin Capabilities

- Add / update / delete products

- Manage categories

- View and manage orders

- Manage users

---

📁 Project Structure

shopkart/
├── shop/
├── cart/
├── orders/
├── templates/
├── static/
├── media/
├── manage.py

---

🚀 Future Enhancements

- Product reviews & ratings

- Coupon / discount system

- Email & SMS notifications

- Order return & refund system

- Cloud deployment (Render / PythonAnywhere)

---

📌 Project Purpose

- This project was developed for:

- Learning Django full-stack development

- Understanding real-world e-commerce workflows

- Academic, portfolio, and resume usage

---

🤝 Contribution

- Contributions are welcome.
- Feel free to fork this repository and submit a pull request.

---

📄 License

This project is created for educational purposes only.

---

👩‍💻 Author

RAMYA DM
GitHub: https://github.com/ramyadurai16

---

✅ GitHub Topics

- django
- python
- ecommerce
- mysql
- bootstrap
- web-development
- django-ecommerce
- razorpay-integration
- full-stack

---
