# UntouchShop

UntouchShop — це сучасний онлайн-магазин парфумерії, створений на Django. Проект включає каталог товарів, кошик, купони на знижку, оформлення замовлення, оплату через Stripe, рекомендації товарів та адмін-панель для керування замовленнями.

## Використані технології

- Python 3.11+
- Django 5.2+
- Stripe API (оплата)
- Celery (асинхронні задачі)
- Redis (брокер для Celery)
- Pillow (робота з зображеннями)
- WeasyPrint (генерація PDF)
- Bootstrap 5 (стилізація інтерфейсу)
- HTML5, CSS3

## Встановлення та запуск

1. **Клонувати репозиторій:**
   ```sh
   git clone https://github.com/Lfhags/django-parfume-site.git
   cd django-parfume-site/untouchshop
   ```

2. **Створити та активувати віртуальне середовище:**
   ```sh
   python -m venv env
   # Windows:
   env\Scripts\activate
   # Linux/Mac:
   source env/bin/activate
   ```

3. **Встановити залежності:**
   ```sh
   pip install -r requirements.txt
   ```
   > Якщо немає requirements.txt, встановіть основні пакети вручну:
   ```sh
   pip install django celery redis stripe pillow weasyprint
   ```

4. **Налаштувати змінні оточення:**
   - Створіть файл `.env` або додайте у `settings.py` змінні для:
     - `SECRET_KEY` (Django)
     - `STRIPE_SECRET_KEY` (Stripe)
     - `STRIPE_PUBLISHABLE_KEY` (Stripe)
     - інші ключі за потреби

5. **Застосувати міграції:**
   ```sh
   python manage.py migrate
   ```

6. **Створити суперкористувача:**
   ```sh
   python manage.py createsuperuser
   ```

7. **Запустити сервер розробки:**
   ```sh
   python manage.py runserver
   ```

8. **(Опційно) Запустити Celery worker:**
   ```sh
   celery -A untouchshop worker -l info
   ```

9. **(Опційно) Запустити Redis:**
   - Для Windows: [Завантажити Redis](https://github.com/microsoftarchive/redis/releases)
   - Для Linux/Mac: `sudo apt install redis-server` або `brew install redis`

---

## Додатково
- Для генерації PDF-рахунків потрібен WeasyPrint та його залежності (див. [офіційну документацію](https://weasyprint.readthedocs.io/en/stable/install.html)).
- Для Stripe використовуйте лише тестові ключі у розробці!

---

**Автор:** Lfhags 