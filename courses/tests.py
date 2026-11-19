import os
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase

from certificates.models import Certificate
from courses.models import Category, Course
from enrollments.models import Enrollment
from quizzes.models import Answer, Question, Quiz


class SeedDemoCommandTests(TestCase):
    def test_seed_demo_is_repeatable_and_creates_learning_data(self):
        admin_env = {
            "DEMO_ADMIN_USERNAME": "seed-admin",
            "DEMO_ADMIN_EMAIL": "admin@example.com",
            "DEMO_ADMIN_PASSWORD": "A-test-only-password-123!",
        }
        with patch.dict(os.environ, admin_env):
            call_command("seed_demo", verbosity=0)
            call_command("seed_demo", verbosity=0)

        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(Course.objects.count(), 3)
        self.assertEqual(Quiz.objects.count(), 3)
        self.assertEqual(Question.objects.count(), 9)
        self.assertEqual(Answer.objects.count(), 36)
        self.assertEqual(Enrollment.objects.count(), 2)
        self.assertEqual(Certificate.objects.count(), 1)
        self.assertTrue(User.objects.get(username="demo").check_password("Demo12345!"))
        self.assertTrue(User.objects.get(username="seed-admin").is_superuser)
