import uuid

from django.contrib.auth.models import User
from django.db import models

from courses.models import Course


class Certificate(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="certificates"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="certificates"
    )
    certificate_number = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.course.title}"
        )