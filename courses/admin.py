from django.contrib import admin
from courses.models import Category, Course, Lesson


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'description']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ['title', 'order', 'duration', 'is_free', 'video_url']
    ordering = ['order']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'level', 'price', 'duration', 'is_active', 'created_at']
    list_filter = ['category', 'level', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-created_at']
    list_editable = ['is_active']
    inlines = [LessonInline]
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = [
        ('Asosiy ma\'lumotlar', {
            'fields': ['title', 'slug', 'category', 'description', 'image']
        }),
        ('Kurs tafsilotlari', {
            'fields': ['level', 'price', 'duration', 'is_active']
        }),
        ('Vaqt belgilari', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'duration', 'is_free']
    list_filter = ['course', 'is_free']
    search_fields = ['title', 'content', 'course__title']
    ordering = ['course', 'order']
    list_editable = ['order', 'is_free']
