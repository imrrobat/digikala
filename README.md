

# 🛒 Shopping Website (Digikala Clone)

A simple shopping website built with **Python** and **Django** for the backend, and **Bootstrap** for the frontend.
This project also integrates with **Zarinpal Payment Gateway** for real-world payment support.

## 🚀 Features

* User authentication (login, signup, logout)
* Product listing and categories
* Shopping cart and order management
* Payment integration with **Zarinpal**
* Responsive design using **Bootstrap**

## 🛠️ Tech Stack

* **Backend:** Python, Django
* **Frontend:** HTML, CSS, Bootstrap
* **Database:** SQLite (default) – can be replaced with PostgreSQL/MySQL
* **Payment:** Zarinpal gateway integration

## 📦 Installation & Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/imrrobat/digikala.git
   cd YourRepo
   ```
2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate   # on Linux/Mac
   venv\Scripts\activate      # on Windows
   ```
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations:

   ```bash
   python manage.py migrate
   ```
5. Create a superuser (for admin panel):

   ```bash
   python manage.py createsuperuser
   ```
6. Run the development server:

   ```bash
   python manage.py runserver
   ```

   Then open: [http://localhost:8000](http://localhost:8000)

## 💳 Payment Setup (Zarinpal)

To enable payments:

* Create an account at [Zarinpal](https://www.zarinpal.com)
* Get your **Merchant ID**
* Add it in the project settings (in `.env` file)

## 📸 Screenshots

*(Add some screenshots of your project here if possible – homepage, product page, cart, checkout, etc.)*

## 🤝 Contributing

Contributions are welcome! Feel free to fork this repo and submit pull requests.

## ⭐ Support

If you like this project, please give it a **star** ⭐ on GitHub — it really helps!

---

می‌خوای من همینو برات فارسی هم آماده کنم (برای مخاطب ایرانی) یا اینکه انگلیسی بمونه بهتره؟
