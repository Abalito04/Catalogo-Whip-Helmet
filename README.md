# 👾 WHIP Helmets — Product Catalog & Management System

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16192?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Cloudinary](https://img.shields.io/badge/Cloudinary-3448C5?style=flat-square&logo=cloudinary&logoColor=white)](https://cloudinary.com/)
[![MercadoPago](https://img.shields.io/badge/MercadoPago-009EE3?style=flat-square&logo=mercadopago&logoColor=white)](https://www.mercadopago.com.ar/)
[![Railway](https://img.shields.io/badge/Deployed%20on-Railway-0B0D0E?style=flat-square&logo=railway&logoColor=white)](https://railway.app/)

> **EN:** A full-stack product catalog and management system for a real motorcycle helmet business. Built with Flask, PostgreSQL, and Cloudinary, it includes an AI-powered background remover for product images, MercadoPago payment integration, user authentication with rate limiting, and a complete admin panel.
>
> **ES:** Sistema completo de catálogo y gestión de productos para un negocio real de cascos de moto. Desarrollado con Flask, PostgreSQL y Cloudinary, incluye eliminación de fondo de imágenes con IA, integración con MercadoPago, autenticación de usuarios con rate limiting y panel de administración completo.

> 📌 **This is a production app used by a real client.** · *Esta app está en producción y la usa un cliente real.*

---

## ✨ Features · Características

### 🛒 Catalog & Store
- Public product catalog with search, filters and availability status
- Product detail pages with image gallery
- WhatsApp / Instagram integration links per product
- Mark products as sold / available with one click

### 👤 User & Auth System
- User registration and login with **Flask-Login**
- Session management and protected routes
- **Rate limiting** with Flask-Limiter to prevent abuse

### 🗣️ Admin Panel
- Add, edit and delete products
- Upload product images to **Cloudinary** (cloud storage)
- **AI-powered background removal** using `rembg` + ONNX Runtime — automatic clean product photos
- Manage product availability and Instagram links
- Database migration scripts included

### 💳 Payments
- **MercadoPago** payment gateway integration

### ☁️ Infrastructure
- **PostgreSQL** database (production on Railway)
- **Cloudinary** for image hosting and transformation
- Deployed on **Railway** with Gunicorn
- Environment variables managed with `python-dotenv`

---

## 🗂️ Project Structure

```
Catalogo-Whip-Helmet/
├── app.py                    # Flask app — all routes and logic
├── models.py                 # SQLAlchemy database models
├── agregar_cascos.py         # Script: bulk add helmets to DB
├── agregar_nuevo_casco.py    # Script: add a single new helmet
├── agregar_link_instagram.py # Script: update Instagram links
├── marcar_vendido.py         # Script: mark helmet as sold
├── marcar_disponible.py      # Script: mark helmet as available
├── migrar.py                 # DB migration script
├── templates/                # Jinja2 HTML templates
├── static/                   # CSS, JS, images
├── requirements.txt
├── Procfile                  # Railway / Gunicorn config
└── runtime.txt
```

---

## 🔧 Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python · Flask 3.1 |
| Database | PostgreSQL · Flask-SQLAlchemy |
| Auth | Flask-Login · Flask-WTF |
| Image Storage | Cloudinary |
| Image AI | rembg · ONNX Runtime (background removal) |
| Payments | MercadoPago API |
| Rate Limiting | Flask-Limiter |
| Frontend | HTML5 · CSS3 · JavaScript · Jinja2 |
| Server | Gunicorn |
| Deployment | Railway |
| Config | python-dotenv |

---

## 🚀 Quick Start · Instalación local

### Prerequisites
- Python 3.8+
- PostgreSQL running locally (or use SQLite for dev)
- Cloudinary account
- MercadoPago developer account

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/Abalito04/Catalogo-Whip-Helmet.git
cd Catalogo-Whip-Helmet

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create a .env file with your credentials
cp .env.example .env  # then fill in your values
```

### Environment Variables

```env
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://user:password@localhost/whip_helmets
CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name
MERCADOPAGO_ACCESS_TOKEN=your_mp_token
```

```bash
# 5. Run the app
python app.py
```

App available at `http://localhost:5000`

---

## 🤖 AI Feature: Background Removal

When adding a new product image, the app automatically removes the background using **[rembg](https://github.com/danielgatis/rembg)** (powered by ONNX Runtime). This gives every helmet photo a clean, professional look without any manual editing.

```python
# Simplified example of how it works
from rembg import remove
from PIL import Image

input_image = Image.open("helmet_photo.jpg")
output_image = remove(input_image)  # Background removed automatically
output_image.save("helmet_clean.png")
```

---

## 💡 What I Learned · Qué aprendí

This is my most complete project — built end-to-end for a **real client currently using it in production**.

- **Database modeling** with Flask-SQLAlchemy and PostgreSQL
- **Cloud image management** with Cloudinary (upload, transform, host)
- **AI integration** in a web app (rembg for background removal)
- **Security**: rate limiting, CSRF protection with Flask-WTF, session management
- **Payment gateway integration** with MercadoPago
- **Production deployment** on Railway with environment variables and Gunicorn
- Writing **DB migration scripts** to evolve the schema without data loss

---

## 👨‍💻 Author

**Matias Abalo** — [@Abalito04](https://github.com/Abalito04)

🌐 [Portfolio](https://matiabalo.up.railway.app/) · ✉️ [abalito95@gmail.com](mailto:abalito95@gmail.com)
