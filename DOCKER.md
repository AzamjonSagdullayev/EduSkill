# EduSkill: Docker orqali ishga tushirish

Ushbu qo'llanma Docker Compose yordamida EduSkill va PostgreSQL'ni ishga tushirish, demo bilan tekshirish hamda serverga joylashni tushuntiradi. Docker Engine va `docker compose` buyrug'i o'rnatilgan bo'lishi kerak.

## 1. Muhit sozlamalari

Loyiha papkasida `.env.example` faylidan `.env` nusxa oling:

```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

`.env` faylida `SECRET_KEY`, `DB_PASSWORD` va `DEMO_ADMIN_PASSWORD` qiymatlarini o'zingizga mos kuchli va noyob qiymatlarga almashtiring. Serverga chiqarishdan avval `ALLOWED_HOSTS` ni domeningiz bilan to'ldiring:

```dotenv
SECRET_KEY=uzun-tasodifiy-maxfiy-kalit
DEBUG=False
ALLOWED_HOSTS=eduskill.example.com
DB_NAME=eduskill
DB_USER=eduskill
DB_PASSWORD=kuchli-va-noyob-parol
DB_HOST=db
DB_PORT=5432
APP_PORT=8000
DEMO_ADMIN_USERNAME=admin
DEMO_ADMIN_EMAIL=admin@eduskill.example.com
DEMO_ADMIN_PASSWORD=admin-uchun-boshqa-kuchli-parol
```

`SECRET_KEY` yaratish uchun PowerShell'da:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

`.env` Git'ga kiritilmaydi. U maxfiy kalitlar va parollarni o'z ichiga oladi.

## 2. Ilovani ishga tushirish

```powershell
docker compose up -d --build
docker compose ps
docker compose logs -f web
```

Web konteyneri PostgreSQL sog'lom holatga kelishini kutadi, migratsiyalarni qo'llaydi, demo ma'lumotlarini yaratadi, statik fayllarni yig'adi va Gunicorn'ni ishga tushiradi. Sahifa:

- Ilova: `http://localhost:8000/`
- Admin panel: `http://localhost:8000/admin/`

Portni o'zgartirish uchun `.env` dagi `APP_PORT` qiymatini kiriting. Server firewall'ida shu portga ruxsat bering yoki ilovani HTTPS reverse proxy ortida ishlating.

## 3. Demo akkauntlar va ma'lumotlar

| Foydalanuvchi | Login | Parol |
|---|---|---|
| O'quvchi | `demo` | `Demo12345!` |
| Admin panel | `.env` dagi `DEMO_ADMIN_USERNAME` | `.env` dagi `DEMO_ADMIN_PASSWORD` |

Demo bazasida 3 ta kurs, 9 ta dars, test savollari, kursga yozilishlar, o'quv progressi, test natijalari va sertifikat yaratiladi. Demo ma'lumotlarini qayta yaratish yoki yangilash uchun:

```powershell
docker compose exec web python manage.py seed_demo
```

Konteynerlar holatini tekshirish:

```powershell
docker compose ps
docker compose logs --tail=100 web
```

## 4. Yangilash va ma'lumotlarni saqlash

Yangi kod bilan qayta build qilish:

```powershell
docker compose up -d --build
```

PostgreSQL ma'lumotlari `postgres_data` nomli Docker volume'da, yuklangan fayllar `media_data` volume'da saqlanadi; konteynerlarni to'xtatish bu ma'lumotlarni o'chirmaydi.

Zaxira nusxa olish (serverda):

```bash
docker compose exec -T db sh -c 'pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB"' > eduskill-backup.sql
```

`docker compose down -v` buyru'i bazani hamda yuklangan fayllarni o'chiradi. Uni faqat ma'lumotlarni butunlay yo'qotish mumkin bo'lganda ishlating.

## 5. Serverga chiqarish

1. Serverga Docker Engine va Docker Compose o'rnating, repository'ni joylashtiring.
2. Serverda `.env` yarating va yuqoridagi maxfiy qiymatlarni server uchun alohida, kuchli qiymatlarga almashtiring.
3. `ALLOWED_HOSTS` ga faqat domeningizni yozing; domen HTTPS bilan reverse proxy ortida bo'lsa, `CSRF_TRUSTED_ORIGINS=https://eduskill.example.com` ni sozlang.
4. Reverse proxy TLS sertifikatini boshqarsin va `X-Forwarded-Proto` sarlavhasini uzatsin. HTTPS yoqilgandan keyin `.env` da `SECURE_SSL_REDIRECT=True`, `SESSION_COOKIE_SECURE=True`, `CSRF_COOKIE_SECURE=True` va `SECURE_HSTS_SECONDS=31536000` qiymatlarini belgilang. HSTS'ni faqat domeningiz HTTPS orqali ishlashiga ishonch hosil qilgach yoqing. Barcha subdomenlar ham HTTPS'da ishlasa, `SECURE_HSTS_INCLUDE_SUBDOMAINS=True` ni qo'shing. `SECURE_HSTS_PRELOAD=True` ni faqat domenni preload ro'yxatiga topshirishga qaror qilganingizda belgilang; preload'dan chiqish uzoq vaqt olishi mumkin.
5. `docker compose up -d --build` bilan ishga tushiring; `docker compose ps` orqali `web` va `db` holati `healthy` ekanini tasdiqlang.
6. `.env` va zaxira nusxalarini web-serverdan ommaga ochmang, ularni Git'ga yuklamang. Default yoki demo parollar bilan ommaviy serverni ishlatmang.

Reverse proxy sozlamasi ushbu Compose fayliga kiritilmagan. Ishlab chiqarish serverida HTTPS/TLS va `/media/` fayllarini taqdim etish uchun Nginx yoki serveringizdagi mavjud proxy'ni sozlang.
