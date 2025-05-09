# EcomVision-project
 An Indian Platform for Product Comparison
EcomVision, a full-stack web application designed to revolutionise the online shopping experience. This project reflects a blend of web scraping, backend automation, full-stack development, and user-focused design. Here’s a breakdown of the tech and skills I put into action:

🔹 Web Scraping & Automation:
Built robust spiders using Scrapy with manual proxies and user-agent rotation
Automated periodic scraping with Celery, ensuring up-to-date pricing and product info

🔹 Backend Engineering:
Developed a scalable backend using Django
Managed user sessions, Google OAuth2 authentication, and OTP-based email login
Enabled full admin CRUD capabilities for products, websites, and categories

🔹 Database Management:
Structured and optimised data storage with PostgreSQL
Implemented relational models for categories like smartphones, laptops, and TVs

🔹 User-Centric Features:
Compare up to 4 products at a time
Track price history with interactive charts
Set price-drop alerts with email notifications
Share products on WhatsApp or buy directly from the original site

🔹 Frontend Development:
Designed clean, responsive UI with HTML, Tailwind CSS, and JavaScript

## Virtual Environment Setup
This project uses a Python virtual environment to manage dependencies. Follow these steps to set up and activate the virtual environment:

### 1. Create a Virtual Environment
Navigate to the project directory and run the following command:

```bash
python -m venv venv
```
### 2. Activate the Virtual Environment
On Windows:
```bash
venv\Scripts\activate.bat
```
On macOS/Linux:
```bash
source venv/bin/activate
```

### 3. Install Required Dependencies (Only First Time Needed)
pip install -r requirements.txt

### 4. Perfrom Django Operations

After activating virtual environment perform the django commands like runserver, collectstatic, etc...

### 5. Deactivating the Virtual Environment

```bash
deactivate
```
