from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from courses.models import Category, Course
from enrollments.models import Enrollment


def home(request):
    popular_courses = Course.objects.filter(is_active=True).select_related('category')[:6]
    categories = Category.objects.all()
    total_courses = Course.objects.filter(is_active=True).count()
    total_categories = categories.count()

    context = {
        'popular_courses': popular_courses,
        'categories': categories,
        'total_courses': total_courses,
        'total_categories': total_categories,
    }
    return render(request, 'home.html', context)


def course_list(request):
    courses = Course.objects.filter(is_active=True).select_related('category')
    categories = Category.objects.all()

    # Qidiruv
    query = request.GET.get('q', '').strip()
    if query:
        courses = courses.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    # Kategoriya filter
    category_slug = request.GET.get('category', '')
    if category_slug:
        courses = courses.filter(category__slug=category_slug)

    # Daraja filter
    level = request.GET.get('level', '')
    if level in ['beginner', 'middle', 'advanced']:
        courses = courses.filter(level=level)

    # Pagination
    paginator = Paginator(courses, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'query': query,
        'selected_category': category_slug,
        'selected_level': level,
        'levels': [('beginner', 'Boshlang\'ich'), ('middle', 'O\'rta'), ('advanced', 'Yuqori')],
    }
    return render(request, 'courses/course_list.html', context)


def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, is_active=True)
    lessons = course.lessons.all()
    quizzes = course.quizzes.filter(is_active=True)

    is_enrolled = False
    enrollment = None
    if request.user.is_authenticated:
        try:
            enrollment = Enrollment.objects.get(user=request.user, course=course)
            is_enrolled = True
        except Enrollment.DoesNotExist:
            pass

    context = {
        'course': course,
        'lessons': lessons,
        'quizzes': quizzes,
        'is_enrolled': is_enrolled,
        'enrollment': enrollment,
        'lesson_count': lessons.count(),
    }
    return render(request, 'courses/course_detail.html', context)


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'courses/category_list.html', {'categories': categories})
