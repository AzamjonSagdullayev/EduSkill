import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from accounts.models import Profile
from certificates.models import Certificate
from courses.models import Category, Course, Lesson
from enrollments.models import Enrollment, LessonProgress
from quizzes.models import Answer, Question, Quiz, QuizResult


COURSES = [
    {
        "category": "Dasturlash",
        "title": "Python dasturlash asoslari",
        "slug": "python-dasturlash-asoslari",
        "description": "Python sintaksisi, funksiyalar va amaliy dasturlash asoslarini o'rganing.",
        "level": "beginner",
        "duration": 12,
        "lessons": [
            ("Python bilan tanishuv", "Python muhiti va birinchi dastur.", True),
            ("O'zgaruvchilar va ma'lumot turlari", "Matn, son va mantiqiy qiymatlar.", True),
            ("Shartlar va sikllar", "Shart operatorlari va takrorlash.", False),
        ],
        "questions": [
            ("Python qaysi turdagi dasturlash tili?", ["Yuqori darajali", "Faqat mashina tili", "Belgilash tili", "Ma'lumotlar bazasi"]),
            ("Python'da matn qiymati qaysi turda saqlanadi?", ["str", "int", "bool", "list"]),
            ("Python'da funksiya e'lon qilish uchun qaysi kalit so'z ishlatiladi?", ["def", "class", "func", "make"]),
        ],
    },
    {
        "category": "Dasturlash",
        "title": "Django bilan web dasturlash",
        "slug": "django-web-dasturlash",
        "description": "Django ORM, sahifalar va URL marshrutlari bilan web ilova tuzing.",
        "level": "middle",
        "duration": 18,
        "lessons": [
            ("Django loyihasini yaratish", "Loyiha tuzilmasi va sozlamalar.", True),
            ("Model va ma'lumotlar bazasi", "Model yaratish va migratsiyalar.", True),
            ("View va URL", "So'rovlarni sahifalar bilan bog'lash.", False),
        ],
        "questions": [
            ("Django'da ma'lumotlar bazasi tuzilmasi qayerda ta'riflanadi?", ["Modelda", "Template'da", "URL'da", "CSS'da"]),
            ("Django migratsiyasi nima uchun kerak?", ["Sxemadagi o'zgarishlarni bazaga qo'llash", "Rasm siqish", "Serverni ishga tushirish", "CSS yaratish"]),
            ("URL so'rovini qayta ishlash mantiqi odatda qayerda yoziladi?", ["View'da", "Modelda", "Static faylda", "Migratsiyada"]),
        ],
    },
    {
        "category": "Dizayn",
        "title": "UI/UX dizayn asoslari",
        "slug": "ui-ux-dizayn-asoslari",
        "description": "Foydalanuvchi tajribasi, wireframe va interfeys dizayni asoslari.",
        "level": "beginner",
        "duration": 10,
        "lessons": [
            ("UI va UX nima?", "Interfeys va foydalanuvchi tajribasi.", True),
            ("Wireframe yaratish", "Sahifa tuzilishini rejalashtirish.", True),
            ("Rang va tipografika", "O'qilishi qulay vizual tizim.", False),
        ],
        "questions": [
            ("Wireframe nima uchun ishlatiladi?", ["Sahifa tuzilishini rejalashtirish", "Server sozlash", "Ma'lumotlar bazasi yaratish", "Kod kompilyatsiyasi"]),
            ("UX dizaynning asosiy maqsadi nima?", ["Foydalanuvchi tajribasini yaxshilash", "Faqat rang tanlash", "Server tezligini o'lchash", "Rasm formatini o'zgartirish"]),
            ("Interfeysda tipografika nimani belgilaydi?", ["Matn ko'rinishi va o'qilishini", "Ma'lumotlar bazasini", "Tarmoq tezligini", "Video formatini"]),
        ],
    },
]

class Command(BaseCommand):
    help = "Demo foydalanuvchilar, kurslar va o'quv ma'lumotlarini yaratadi."

    @transaction.atomic
    def handle(self, *args, **options):
        admin_username = os.environ.get("DEMO_ADMIN_USERNAME", "").strip()
        if admin_username:
            self._ensure_admin(admin_username)

        learner, created = User.objects.get_or_create(
            username="demo",
            defaults={
                "email": "demo@example.com",
                "first_name": "Demo",
                "last_name": "O'quvchi",
            },
        )
        if created:
            learner.set_password("Demo12345!")
            learner.save(update_fields=["password"])
        Profile.objects.get_or_create(user=learner, defaults={"bio": "EduSkill demo o'quvchisi."})

        categories = {}
        for name, slug, description in [
            ("Dasturlash", "dasturlash", "Dasturlash va web texnologiyalari."),
            ("Dizayn", "dizayn", "Raqamli mahsulotlar uchun dizayn."),
        ]:
            categories[name], _ = Category.objects.update_or_create(
                slug=slug,
                defaults={"name": name, "description": description},
            )

        course_objects = []
        for item in COURSES:
            course, _ = Course.objects.update_or_create(
                slug=item["slug"],
                defaults={
                    "category": categories[item["category"]],
                    "title": item["title"],
                    "description": item["description"],
                    "price": 0,
                    "duration": item["duration"],
                    "level": item["level"],
                    "is_active": True,
                },
            )
            lessons = []
            for order, (title, description, is_free) in enumerate(item["lessons"], start=1):
                lesson, _ = Lesson.objects.update_or_create(
                    course=course,
                    order=order,
                    defaults={
                        "title": title,
                        "description": description,
                        "content": description,
                        "duration": 20 + order * 5,
                        "is_free": is_free,
                    },
                )
                lessons.append(lesson)
            course_objects.append((course, lessons))

            quiz, _ = Quiz.objects.update_or_create(
                course=course,
                defaults={
                    "lesson": lessons[0],
                    "title": f"{course.title}: bilimlar testi",
                    "description": "Kurs mavzularini takrorlash uchun demo test.",
                    "time_limit": 10,
                    "is_active": True,
                },
            )
            for order, (text, choices) in enumerate(item["questions"], start=1):
                question, _ = Question.objects.update_or_create(
                    quiz=quiz,
                    order=order,
                    defaults={"text": text},
                )
                for answer_order, answer_text in enumerate(choices):
                    Answer.objects.update_or_create(
                        question=question,
                        text=answer_text,
                        defaults={"is_correct": answer_order == 0},
                    )

        ongoing_course, ongoing_lessons = course_objects[0]
        ongoing_enrollment, _ = Enrollment.objects.get_or_create(
            user=learner,
            course=ongoing_course,
        )
        for lesson in ongoing_lessons[:2]:
            LessonProgress.objects.update_or_create(
                enrollment=ongoing_enrollment,
                lesson=lesson,
                defaults={"completed": True, "completed_at": timezone.now()},
            )
        ongoing_enrollment.progress = 66
        ongoing_enrollment.completed = False
        ongoing_enrollment.completed_at = None
        ongoing_enrollment.save(update_fields=["progress", "completed", "completed_at"])

        completed_course, completed_lessons = course_objects[1]
        completed_enrollment, _ = Enrollment.objects.get_or_create(
            user=learner,
            course=completed_course,
        )
        for lesson in completed_lessons:
            LessonProgress.objects.update_or_create(
                enrollment=completed_enrollment,
                lesson=lesson,
                defaults={"completed": True, "completed_at": timezone.now()},
            )
        completed_enrollment.progress = 100
        completed_enrollment.completed = True
        completed_enrollment.completed_at = completed_enrollment.completed_at or timezone.now()
        completed_enrollment.save(update_fields=["progress", "completed", "completed_at"])
        Certificate.objects.get_or_create(user=learner, course=completed_course)

        for course, _lessons in course_objects[:2]:
            quiz = Quiz.objects.get(course=course)
            QuizResult.objects.update_or_create(
                user=learner,
                quiz=quiz,
                defaults={
                    "score": 2,
                    "total_questions": 3,
                    "percentage": 67,
                    "passed": False,
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Demo ma'lumotlari tayyor: {len(course_objects)} kurs, "
                f"demo foydalanuvchi: demo / Demo12345!; "
                f"admin: {admin_username or 'sozlanmagan'}."
            )
        )

    def _ensure_admin(self, username):
        password = os.environ.get("DEMO_ADMIN_PASSWORD", "")
        email = os.environ.get("DEMO_ADMIN_EMAIL", "")
        if not password or not email:
            raise CommandError(
                "Admin yaratish uchun DEMO_ADMIN_PASSWORD va DEMO_ADMIN_EMAIL kerak."
            )
        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email, "is_staff": True, "is_superuser": True},
        )
        if created:
            user.set_password(password)
            user.save(update_fields=["password"])
        elif not (user.is_staff and user.is_superuser):
            raise CommandError(
                f"'{username}' foydalanuvchisi admin emas; admin username qiymatini o'zgartiring."
            )
