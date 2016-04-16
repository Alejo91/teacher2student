from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import SchoolUser

class UsersTests(TestCase):

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

    def test_users(self):
        self.assertTrue(isinstance(self.student, SchoolUser))
        self.assertTrue(isinstance(self.teacher, SchoolUser))
        self.assertEqual(
            self.student.__str__(),
            "%s %s" % (self.student.first_name, self.student.last_name)
        )
        self.assertEqual(
            self.teacher.__str__(),
            "%s %s" % (self.teacher.first_name, self.teacher.last_name)
        )

    def test_type(self):
        self.assertTrue(self.student.is_student())
        self.assertFalse(self.student.is_teacher())
        self.assertTrue(self.teacher.is_teacher())
        self.assertFalse(self.teacher.is_student())

    def test_url(self):
        self.assertEqual(
            self.student.get_homework_url(),
            reverse('homework:student_list_homework')
        )
        self.assertEqual(
            self.teacher.get_homework_url(),
            reverse('homework:list')
        )
