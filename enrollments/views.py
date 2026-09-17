from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from certificates.models import Certificate
from courses.models import Course, Lesson
from enrollments.models import Enrollment, LessonProgress
from quizzes.models import QuizResult


@login_required
def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id, is_active=True)

    if request.method == 'POST':
        try:
            Enrollment.objects.create(user=request.user, course=course)
            messages.success(request, f'"{course.title}" kursiga muvaffaqiyatli yozildingiz!')
        except IntegrityError:
            messages.warning(request, 'Siz bu kursga allaqachon yozilgansiz.')
        return redirect('courses:course_detail', slug=course.slug)

    return redirect('courses:course_detail', slug=course.slug)


@login_required
def dashboard(request):
    enrollments = Enrollment.objects.filter(
        user=request.user
    ).select_related('course', 'course__category')

    certificates = Certificate.objects.filter(
        user=request.user
    ).select_related('course')

    # Statistika
    total_enrolled = enrollments.count()
    completed_count = enrollments.filter(completed=True).count()
    in_progress_count = enrollments.filter(completed=False).count()
    certs_count = certificates.count()

    # O'rtacha quiz natijasi
    quiz_results = QuizResult.objects.filter(user=request.user)
    avg_score = 0
    if quiz_results.exists():
        total_pct = sum(r.percentage for r in quiz_results)
        avg_score = round(total_pct / quiz_results.count())

    context = {
        'enrollments': enrollments,
        'certificates': certificates,
        'total_enrolled': total_enrolled,
        'completed_count': completed_count,
        'in_progress_count': in_progress_count,
        'certs_count': certs_count,
        'avg_score': avg_score,
    }
    return render(request, 'enrollments/dashboard.html', context)


@login_required
def lesson_detail(request, course_slug, lesson_id):
    course = get_object_or_404(Course, slug=course_slug, is_active=True)

    # Faqat yozilgan userlar darsni ko'ra oladi
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)

    lesson = get_object_or_404(Lesson, pk=lesson_id, course=course)

    # Oldingi va keyingi darslar
    all_lessons = list(course.lessons.all())
    current_index = next((i for i, l in enumerate(all_lessons) if l.pk == lesson.pk), 0)
    prev_lesson = all_lessons[current_index - 1] if current_index > 0 else None
    next_lesson = all_lessons[current_index + 1] if current_index < len(all_lessons) - 1 else None

    # Dars holati
    lesson_progress, _ = LessonProgress.objects.get_or_create(
        enrollment=enrollment,
        lesson=lesson
    )

    # Kurs quizlari
    quiz = getattr(lesson, 'quiz', None)

    context = {
        'course': course,
        'lesson': lesson,
        'enrollment': enrollment,
        'lesson_progress': lesson_progress,
        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson,
        'all_lessons': all_lessons,
        'quiz': quiz,
    }
    return render(request, 'enrollments/lesson_detail.html', context)


@login_required
def complete_lesson(request, course_slug, lesson_id):
    if request.method != 'POST':
        return redirect('enrollments:lesson_detail', course_slug=course_slug, lesson_id=lesson_id)

    course = get_object_or_404(Course, slug=course_slug, is_active=True)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
    lesson = get_object_or_404(Lesson, pk=lesson_id, course=course)

    lesson_progress, created = LessonProgress.objects.get_or_create(
        enrollment=enrollment,
        lesson=lesson
    )

    if not lesson_progress.completed:
        lesson_progress.completed = True
        lesson_progress.completed_at = timezone.now()
        lesson_progress.save()

        # Progress hisoblash
        enrollment.calculate_progress()

        # Kurs tugagan bo'lsa sertifikat yaratish
        enrollment.refresh_from_db()
        if enrollment.completed:
            _issue_certificate_if_eligible(request.user, course, enrollment)

        messages.success(request, f'"{lesson.title}" darsi tugatildi!')
    else:
        messages.info(request, 'Bu dars allaqachon tugatilgan.')

    # Keyingi darsga o'tish
    all_lessons = list(course.lessons.all())
    current_index = next((i for i, l in enumerate(all_lessons) if l.pk == lesson.pk), 0)
    if current_index < len(all_lessons) - 1:
        next_lesson = all_lessons[current_index + 1]
        return redirect('enrollments:lesson_detail', course_slug=course_slug, lesson_id=next_lesson.pk)

    messages.success(request, f'Tabriklaymiz! "{course.title}" kursini tugatdingiz!')
    return redirect('courses:course_detail', slug=course_slug)


def _issue_certificate_if_eligible(user, course, enrollment):
    """Kurs tugaganda sertifikat beriladi."""
    if not Certificate.objects.filter(user=user, course=course).exists():
        Certificate.objects.create(user=user, course=course)
