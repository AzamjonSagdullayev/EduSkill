from django.contrib import admin
from enrollments.models import Enrollment, LessonProgress


class LessonProgressInline(admin.TabularInline):
    model = LessonProgress
    extra = 0
    readonly_fields = ['lesson', 'completed', 'completed_at']
    can_delete = False


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'progress', 'completed', 'enrolled_at', 'completed_at']
    list_filter = ['completed', 'enrolled_at', 'course']
    search_fields = ['user__username', 'course__title']
    ordering = ['-enrolled_at']
    readonly_fields = ['enrolled_at', 'completed_at', 'progress']
    inlines = [LessonProgressInline]


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'lesson', 'completed', 'completed_at']
    list_filter = ['completed']
    search_fields = ['enrollment__user__username', 'lesson__title']
    readonly_fields = ['completed_at']
