from datetime import datetime
from django.test import TestCase
from .models import Homework, Answer
from users.models import SchoolUser

class HomeworkTest(TestCase):
    """Test models of the homework app."""

    def setUp(self):
        """Create a user of each different type."""
        self.student = SchoolUser.objects.create(
            username='student@test.com',
            email='student@test.com',
            user_type='student',
            first_name='Jack',
            last_name='Student',
        )
        self.teacher = SchoolUser.objects.create(
            username='teacher@test.com',
            email='teacher@test.com',
            user_type='teacher',
            first_name='John',
            last_name='Teacher',
        )
        self.homework = Homework.objects.create(
            title='Homework #1',
            question='How are you?',
            teacher=self.teacher,
            due_date= datetime.now(),
        )
        self.answer = Answer.objects.create(
            description='Great!',
            homework=self.homework,
            student = self.student
        )

    def test_homework(self):
        self.assertEqual(str(self.homework),
                         self.homework.title)
        self.assertTrue(self.homework.has_answered(self.student))
        self.homework.student.add(self.student)
        self.homework.save()
        self.answer.student = self.student
        self.answer.save()
        self.assertTrue(self.homework.has_answered(self.student))

    def test_answer(self):
        self.assertEqual(str(self.answer),
                         str(self.answer.id))
