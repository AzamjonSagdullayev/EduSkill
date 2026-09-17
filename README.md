# 🎓 EduSkill

**EduSkill** — zamonaviy kasblarni o‘rganishni istagan yoshlar uchun yaratilgan zamonaviy ta’lim platformasi.

Platforma orqali foydalanuvchilar turli yo‘nalishlardagi kurslarni ko‘rishi, kurslarga yozilishi, darslarni o‘rganishi, testlardan o‘tishi, o‘z progressini kuzatishi va kursni muvaffaqiyatli tugatgandan so‘ng sertifikat olishi mumkin.

---

## 👨‍💻 Author

**Azamjon Sagdullayev**

---

## 🚀 Project haqida

EduSkill foydalanuvchilarga zamonaviy kasblarni tizimli ravishda o‘rganish imkonini beruvchi online learning platforma sifatida ishlab chiqilgan.

Platformada:

* 📚 Zamonaviy kasblar bo‘yicha kurslar
* 📂 Kurs kategoriyalari
* 📖 Kurs darslari
* 🎥 Video va o‘quv materiallari
* 📝 Interaktiv testlar
* 📊 O‘quv progressi
* 👤 Shaxsiy profil
* 📈 Dashboard
* 🏆 Sertifikatlar
* 🔐 Authentication
* 🛠 Django Admin

mavjud.

---

# ✨ Asosiy imkoniyatlar

## 🔐 Authentication

Foydalanuvchilar:

* Ro‘yxatdan o‘tish
* Tizimga kirish
* Tizimdan chiqish
* Profil ma’lumotlarini boshqarish
* Avatar yuklash

imkoniyatlariga ega.

---

## 📚 Courses

Foydalanuvchilar mavjud kurslarni ko‘rishi mumkin.

Har bir kursda:

* Kurs nomi
* Tavsif
* Kategoriya
* Daraja
* Davomiyligi
* Narxi
* Kurs rasmi
* Darslar soni

ko‘rsatiladi.

Kurslarni:

* 🔎 qidirish
* 📂 kategoriya bo‘yicha filtrlash
* 📊 daraja bo‘yicha filtrlash

mumkin.

---

## 📖 Lessons

Har bir kurs bir nechta darslardan tashkil topadi.

Darslarda:

* Dars nomi
* Video
* O‘quv materiali
* Davomiyligi
* Oldingi dars
* Keyingi dars

mavjud.

Foydalanuvchi darsni tugatganini belgilashi mumkin.

---

## 📊 Progress System

Platforma foydalanuvchining kurs bo‘yicha progressini avtomatik hisoblaydi.

Masalan:

```text
Python Backend

██████████████░░░░░░ 70%

Progress: 70%
```

Kursdagi tugatilgan darslar soniga qarab progress avtomatik yangilanadi.

---

## 📝 Quiz System

Har bir kurs uchun testlar mavjud.

Test davomida:

* Savollar
* Javob variantlari
* Vaqt chegarasi
* Natija

mavjud.

Test tugagandan keyin foydalanuvchiga:

```text
Score: 8 / 10
Percentage: 80%
Status: Passed
```

kabi natija ko‘rsatiladi.

Passing score:

```text
70%
```

---

## 🏆 Certificate

Foydalanuvchi kursni muvaffaqiyatli tugatgandan so‘ng sertifikat olishi mumkin.

Sertifikatda:

* Foydalanuvchi ismi
* Kurs nomi
* Sertifikat raqami
* Berilgan sana

ko‘rsatiladi.

Sertifikatni print qilish imkoniyati ham mavjud.

---

# 👤 Dashboard

Har bir foydalanuvchi shaxsiy dashboardga ega.

Dashboardda:

### 📚 My Courses

Foydalanuvchining yozilgan kurslari.

### 📈 Progress

Har bir kurs bo‘yicha o‘rganish darajasi.

### 📝 Quiz Results

Topshirilgan testlar va natijalar.

### 🏆 Certificates

Olingan sertifikatlar.

### 📊 Statistics

* Enrolled courses
* Completed courses
* In progress
* Certificates
* Average quiz score

ko‘rsatiladi.

---

# 🛠 Admin Panel

Django Admin orqali administrator platformadagi asosiy ma’lumotlarni boshqarishi mumkin.

Administrator:

* Categories
* Courses
* Lessons
* Enrollments
* Quizzes
* Questions
* Answers
* Quiz Results
* Certificates
* Users

ni boshqarishi mumkin.

---

# 💻 Texnologiyalar

## Backend

* Python
* Django
* Django ORM

## Frontend

* HTML5
* CSS3
* JavaScript
* Django Templates

## Database

* PostgreSQL

## Additional

* Pillow
* Django Authentication
* Django Messages Framework

---

# 🏗 Project Structure

```text
eduskill/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── accounts/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
│
├── courses/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
│
├── enrollments/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── quizzes/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
│
├── certificates/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── accounts/
│   ├── courses/
│   ├── enrollments/
│   ├── quizzes/
│   ├── certificates/
│   └── partials/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/
│
├── manage.py
├── requirements.txt
├── .env
└── README.md
```

---

# ⚙️ Installation

## 1. Repository'ni clone qilish

```bash
git clone https://github.com/AzamjonSagdullayev/EduSkill
cd eduskill
```

## 2. Virtual environment yaratish

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

## 3. Dependencies o‘rnatish

```bash
pip install -r requirements.txt
```

---

# 🗄 PostgreSQL Configuration

PostgreSQL database yaratish:

```sql
CREATE DATABASE eduskill;
```

`.env` fayl:

```env
SECRET_KEY=your-secret-key
DEBUG=True

DB_NAME=eduskill
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

---

# 🔄 Migrations

Database migrationlarini yaratish:

```bash
python manage.py makemigrations
```

Migrationlarni qo‘llash:

```bash
python manage.py migrate
```

---

# 👑 Superuser yaratish

Django Admin uchun:

```bash
python manage.py createsuperuser
```

Username, email va password kiriting.


Bu development uchun boshlang‘ich:

* kategoriyalar
* kurslar
* darslar
* quizlar
* savollar

yaratadi.

---

# ▶️ Loyihani ishga tushirish

```bash
python manage.py runserver
```

Keyin browser orqali:

```text
http://127.0.0.1:8000/
```

manziliga kiring.

Admin panel:

```text
http://127.0.0.1:8000/admin/
```

---

# 🔒 Security

Loyihada quyidagi xavfsizlik mexanizmlaridan foydalaniladi:

* Django CSRF Protection
* Authentication
* Authorization
* Login Required
* Form Validation
* Password Hashing
* User permission checking
* Environment Variables

Maxfiy ma’lumotlar `.env` faylida saqlanishi kerak.

`.env` Git repository'ga yuklanmasligi kerak.

---

# 📱 Responsive Design

EduSkill turli qurilmalarda ishlashga moslashtirilgan:

```text
📱 Mobile
   ↓
📱 Tablet
   ↓
💻 Laptop
   ↓
🖥 Desktop
```

---

# 🎯 Project Goals

EduSkill loyihasining asosiy maqsadi:

> Yoshlarni zamonaviy kasblarga qiziqtirish va ularga bilim olish uchun qulay raqamli platforma yaratish.

Platforma kelajakda quyidagi yo‘nalishlarni qamrab olishi mumkin:

* 🐍 Python
* 🌐 Web Development
* 🤖 Artificial Intelligence
* 🎨 UI/UX Design
* 📱 Mobile Development
* 📊 Data Analytics
* 📣 SMM
* 🎬 Video Editing
* 🎨 Graphic Design

---

# 🔮 Future Improvements

Kelajakda quyidagi imkoniyatlar qo‘shilishi mumkin:

* 🤖 AI-powered learning assistant
* 💬 Course comments
* ⭐ Course rating
* 🔔 Notifications
* 📧 Email verification
* 🔑 Password reset
* 💳 Online payment
* 🎓 Advanced certificates
* 📊 Advanced analytics
* 🏅 Achievement system
* 🌍 Multiple languages
* 📱 PWA support

---

# 📸 Screenshots

Loyiha ishga tayyor bo‘lgach, bu bo‘limga platformaning asosiy sahifalari screenshotlari qo‘shiladi.

```text
Home
Courses
Course Detail
Dashboard
Quiz
Certificate
Admin Panel
```

---

# 📄 License

This project is developed for educational and demonstration purposes.

---

## 👨‍💻 Developer

**Azamjon Sagdullayev**

> Building modern web applications with Python and Django.
