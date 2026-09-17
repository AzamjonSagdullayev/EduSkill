from django.contrib import admin
from quizzes.models import Quiz, Question, Answer, QuizResult


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4
    fields = ['text', 'is_correct']


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 2
    fields = ['text', 'order']
    ordering = ['order']


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'lesson', 'time_limit', 'is_active']
    list_filter = ['is_active', 'course']
    search_fields = ['title', 'course__title']
    list_editable = ['is_active']
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'quiz', 'order']
    list_filter = ['quiz']
    search_fields = ['text', 'quiz__title']
    ordering = ['quiz', 'order']
    inlines = [AnswerInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['text', 'question', 'is_correct']
    list_filter = ['is_correct', 'question__quiz']
    search_fields = ['text']
    list_editable = ['is_correct']


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'score', 'total_questions', 'percentage', 'passed', 'completed_at']
    list_filter = ['passed', 'completed_at']
    search_fields = ['user__username', 'quiz__title']
    ordering = ['-completed_at']
    readonly_fields = ['completed_at']
