from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from enrollments.models import Enrollment
from quizzes.forms import QuizSubmitForm
from quizzes.models import Quiz, QuizResult, Answer


@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id, is_active=True)

    # Foydalanuvchi kursga yozilganligini tekshirish
    enrollment = get_object_or_404(Enrollment, user=request.user, course=quiz.course)

    questions = quiz.questions.prefetch_related('answers').all()

    if not questions.exists():
        messages.warning(request, 'Bu quizda hali savollar yo\'q.')
        return redirect('courses:course_detail', slug=quiz.course.slug)

    if request.method == 'POST':
        form = QuizSubmitForm(questions, request.POST)
        if form.is_valid():
            score = 0
            total = questions.count()

            for question in questions:
                selected_answer_id = form.get_answer_for_question(question.pk)
                try:
                    selected_answer = Answer.objects.get(pk=int(selected_answer_id))
                    if selected_answer.is_correct:
                        score += 1
                except (Answer.DoesNotExist, (ValueError, TypeError)):
                    pass

            percentage = int((score / total) * 100) if total > 0 else 0
            passed = percentage >= 70

            result = QuizResult.objects.create(
                user=request.user,
                quiz=quiz,
                score=score,
                total_questions=total,
                percentage=percentage,
                passed=passed,
            )

            if passed:
                messages.success(request, f'Tabriklaymiz! Quiz muvaffaqiyatli topshirildi. {score}/{total}')
            else:
                messages.warning(request, f'Test topshirildi, lekin o\'tmadingiz. {score}/{total} — {percentage}%')

            return redirect('quizzes:quiz_result', result_id=result.pk)
        else:
            messages.error(request, 'Iltimos, barcha savollarga javob bering.')
    else:
        form = QuizSubmitForm(questions)

    context = {
        'quiz': quiz,
        'form': form,
        'questions': questions,
    }
    return render(request, 'quizzes/quiz_detail.html', context)


@login_required
def quiz_result(request, result_id):
    result = get_object_or_404(QuizResult, pk=result_id, user=request.user)

    context = {
        'result': result,
        'quiz': result.quiz,
    }
    return render(request, 'quizzes/quiz_result.html', context)
