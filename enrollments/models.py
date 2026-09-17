from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from courses.models import Course, Lesson


class Enrollment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    progress = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'course'],
                name='unique_user_course'
            )
        ]
        ordering = ['-enrolled_at']

    def __str__(self):
        return f'{self.user.username} - {self.course.title}'

    def calculate_progress(self):
        """Haqiqiy progressni hisoblaydi va saqlaydi."""
        total = self.course.lessons.count()
        if total == 0:
            return 0
        completed = self.lesson_progresses.filter(completed=True).count()
        progress = int((completed / total) * 100)
        self.progress = progress
        if progress == 100:
            self.completed = True
            if not self.completed_at:
                self.completed_at = timezone.now()
        self.save(update_fields=['progress', 'completed', 'completed_at'])
        return progress


class LessonProgress(models.Model):
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name='lesson_progresses'
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='lesson_progresses'
    )
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['enrollment', 'lesson'],
                name='unique_enrollment_lesson'
            )
        ]

    def __str__(self):
        return f'{self.enrollment.user.username} - {self.lesson.title}'