from datetime import datetime, date

from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse

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
        self.student.set_password("1234")
        self.student.save()
        self.teacher = SchoolUser.objects.create(
            username='teacher@test.com',
            email='teacher@test.com',
            user_type='teacher',
            first_name='John',
            last_name='Teacher',
        )
        self.teacher.set_password("1234")
        self.teacher.save()
        self.anonymous = AnonymousUser()
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

    def get_response(self, user, url, method, post_data={}):
        """Helper function to perform HTTP request with user."""
        if not user.is_anonymous():
            self.client.login(username=user.username, password="1234")
        if method == 'GET':
            response = self.client.get(url)
        elif method == 'POST':
            response = self.client.post(url, post_data)
        return response

    def render_page(self, user, url, expected_status_code, redirect_url=None):
        """Helper function to test page rendering."""
        response = self.get_response(user, url, 'GET')
        resp_status_code = response.status_code
        self.assertEqual(expected_status_code, resp_status_code)
        if resp_status_code == 302 and redirect_url:
            self.assertRedirects(response, redirect_url)

    def post_data_to_page(self, user, url, post_data, expected_status_code,
                          redirect_url=None):
        """Helper function to test posting data to page."""
        response = self.get_response(user, url, 'POST', post_data=post_data)
        resp_status_code = response.status_code
        self.assertEqual(expected_status_code, resp_status_code)
        if resp_status_code == 302 and redirect_url:
            self.assertRedirects(response, redirect_url)

    def test_homework_create(self):
        """Test homework create view rendering and post."""
        # Try to access page with invalid user profile
        self.render_page(self.student, reverse('homework:create'), 403)
        self.render_page(self.anonymous, reverse('homework:create'), 403,
                         reverse('users:signin'))
        # Access page as a Teacher & post data to create homework
        self.render_page(self.teacher, reverse('homework:create'), 200)
        post_data = {
            'title': 'Homework #2',
            'question': "What's your name?",
            'due_date': date.today(),
            'teacher': self.teacher.id,
        }
        self.post_data_to_page(self.teacher, reverse('homework:create'),
                               post_data, 302, reverse('homework:list'))

    def test_homework_update(self):
        """Test homework update view rendering and post."""
        # Try to access page with invalid user profile
        self.render_page(self.student,
                         reverse('homework:update',
                                 kwargs={'pk': self.homework.pk}),
                         403)
        self.render_page(self.anonymous,
                         reverse('homework:update',
                                 kwargs={'pk': self.homework.pk}),
                         403, reverse('users:signin'))
        # Access page as a Teacher & post data to update homework
        self.render_page(self.teacher,
                         reverse('homework:update',
                                 kwargs={'pk': self.homework.pk}),
                         200)
        post_data = {
            'title': 'Homework #1 updated',
            'question': "What's your name?",
            'due_date': date.today(),
            'teacher': self.teacher.id,
        }
        self.post_data_to_page(self.teacher,
                               reverse('homework:update',
                                   kwargs={'pk': self.homework.pk}),
                               post_data, 302, reverse('homework:list'))
        updated_homework = Homework.objects.get(id=self.homework.id)
        self.assertEqual(updated_homework.title, post_data['title'])

    def test_homework_assign(self):
        """Test Homework assign view rendering."""
        # Try to access page with invalid user profile
        self.render_page(self.student,
                         reverse('homework:assign_student_list',
                                 kwargs={'pk': self.homework.pk}),
                         403)
        self.render_page(self.anonymous,
                         reverse('homework:assign_student_list',
                                 kwargs={'pk': self.homework.pk}),
                         403, reverse('users:signin'))
        # Access page as a Teacher
        self.render_page(self.teacher,
                         reverse('homework:assign_student_list',
                                 kwargs={'pk': self.homework.pk}),
                         200)

    def test_homework_add(self):
        """Test associating student to homework"""
        # Check that student is not associated
        student_assigned = self.student in self.homework.student.all()
        self.assertFalse(student_assigned)
        # Assign student
        post_data = {
            'homework_id': self.homework.id,
            'student_id': self.student.id,
        }
        self.post_data_to_page(self.teacher,
                               reverse('homework:add_student'),
                               post_data, 200)
        # Check if new student has been associated
        student_assigned = self.student in self.homework.student.all()
        self.assertTrue(student_assigned)


    def test_homework_remove(self):
        """Test removing student assignement"""
        self.homework.student.add(self.student)
        # Check that student is assigned
        student_assigned = self.student in self.homework.student.all()
        self.assertTrue(student_assigned)
        post_data = {
            'homework_id': self.homework.id,
            'student_id': self.student.id,
        }
        self.post_data_to_page(self.teacher,
                               reverse('homework:remove_student'),
                               post_data, 200)
        # Check if student has been removed 
        student_assigned = self.student in self.homework.student.all()
        self.assertFalse(student_assigned)

    def test_student_answers(self):
        """Test Homework student's answers view rendering."""
        # Try to access page with invalid user profile
        self.render_page(self.student,
                         reverse('homework:student_answers',
                                  kwargs={
                                      'pk': self.homework.id,
                                      'student': self.student.id
                                  }),
                         403)
        self.render_page(self.anonymous,
                         reverse('homework:student_answers',
                                  kwargs={
                                      'pk': self.homework.id,
                                      'student': self.student.id
                                  }),
                         403, reverse('users:signin'))
        # Access page as a Teacher & post data to create homework
        self.render_page(self.teacher,
                         reverse('homework:student_answers',
                                  kwargs={
                                      'pk': self.homework.id,
                                      'student': self.student.id
                                  }),
                         200)

    def test_latest_answers(self):
        """Test Homework latest answers view rendering."""
        # Try to access page with invalid user profile
        self.render_page(self.student,
                         reverse('homework:latest_answers',
                                 kwargs={'pk': self.homework.pk}),
                         403)
        self.render_page(self.anonymous,
                         reverse('homework:latest_answers',
                                 kwargs={'pk': self.homework.pk}),
                         403, reverse('users:signin'))
        # Access page as a Teacher & post data to create homework
        self.render_page(self.teacher,
                         reverse('homework:latest_answers',
                                 kwargs={'pk': self.homework.pk}),
                         200)

    def test_homework_list(self):
        """Test student Homework list view rendering."""
        # Try to access page with invalid user profile
        self.render_page(self.teacher, reverse('homework:student_list_homework'), 403)
        self.render_page(self.anonymous, reverse('homework:student_list_homework'), 403,
                         reverse('users:signin'))
        # Access page as a Student
        self.render_page(self.student, reverse('homework:student_list_homework'), 200)

    def test_answer_create(self):
        """Test student Answer create view rendering and post."""
        # Try to access page with invalid user profile
        self.render_page(self.teacher,
                         reverse('homework:new_answer',
                                 kwargs={'pk': self.homework.id}),
                         403)
        self.render_page(self.anonymous,
                         reverse('homework:new_answer',
                                 kwargs={'pk': self.homework.id}),
                         403, reverse('users:signin'))
        # Access page as a Student
        self.render_page(self.student,
                         reverse('homework:new_answer',
                                 kwargs={'pk': self.homework.id}),
                         200)
        # Post new answer
        post_data = {
            'description': 'This is my second answer',
            'student': self.student.id,
            'homework': self.homework.id,
        }
        self.post_data_to_page(self.student,
                               reverse('homework:new_answer',
                                   kwargs={'pk': self.homework.id}),
                               post_data, 302,
                               reverse('homework:student_list_homework'))
        last_answer = self.student.answer_set.last()
        self.assertEqual(last_answer.description, post_data['description'])
