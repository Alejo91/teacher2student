from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import SchoolUser

class UsersTests(TestCase):

    def setUp(self):
        """Set up some data and urls for tests."""
        self.student = SchoolUser.objects.create(
            username='student@test.com',
            email='student@test.com',
            user_type='student',
            first_name='Jack',
            last_name='Student',
        )
        self.student.set_password('1234')
        self.student.save()
        self.teacher = SchoolUser.objects.create(
            username='teacher@test.com',
            email='teacher@test.com',
            user_type='teacher',
            first_name='John',
            last_name='Teacher',
        )
        self.teacher.set_password('1234')
        self.teacher.save()
        self.signup_url = reverse('users:student_signup')
        self.signin_url = reverse('users:signin')
        self.update_url = reverse('users:profile')


    def test_student_signup(self):
        """Test view for student Signup."""
        post = {'email': 'student1@test.com', 'first_name': 'Tom',
                'last_name': 'Student', 'user_type': 'student',
                'password': '1234'}
        response = self.client.post(self.signup_url, post)
        self.assertRedirects(response, reverse('home'))
        SchoolUser.objects.get(username='student1@test.com')

    def test_teacher_signup(self):
        """Test view for teacher Signup."""
        post = {'email': 'teacher1@test.com', 'first_name': 'Tim',
                'last_name': 'Teacher', 'user_type': 'teacher',
                'password': '1234'}
        response = self.client.post(self.signup_url, post)
        self.assertRedirects(response, reverse('home'))
        SchoolUser.objects.get(username='teacher1@test.com')

    def test_student_login(self):
        """Test view for student Signin."""
        # Test classic login
        post = {'username_or_email': 'student@test.com', 'password': '1234'}
        response = self.client.post(self.signin_url, post)
        self.assertRedirects(response, reverse('home'))
        # Test login with next page
        response = self.client.post(
            self.signin_url + '?next=' +  self.student.get_homework_url(),
            post)
        self.assertRedirects(response, self.student.get_homework_url())
        # Logout View
        response = self.client.get(reverse('users:logout'))
        self.assertRedirects(response, reverse('home'))
        # Try access homework page not logged in
        response = self.client.get(self.student.get_homework_url())
        redirect_url = self.signin_url + '?next=' + self.student.get_homework_url()
        self.assertRedirects(response, redirect_url)

    def test_teacher_login_logout(self):
        """Test view for student Signin."""
        # Test classic login
        post = {'username_or_email': 'teacher@test.com', 'password': '1234'}
        response = self.client.post(self.signin_url, post)
        self.assertRedirects(response, reverse('home'))
        # Logout
        self.client.logout()
        # Test login with next page
        response = self.client.post(
            self.signin_url + '?next=' + self.teacher.get_homework_url(),
            post)
        self.assertRedirects(response, self.teacher.get_homework_url())
        response = self.client.get(self.teacher.get_homework_url())
        self.assertEqual(response.status_code, 200)
        # Logout View
        response = self.client.get(reverse('users:logout'))
        self.assertRedirects(response, reverse('home'))
        # Try access homework page not logged in
        response = self.client.get(self.teacher.get_homework_url())
        redirect_url = self.signin_url + '?next=' + self.teacher.get_homework_url()
        self.assertRedirects(response, redirect_url)

    def test_user_update(self):
        """Test view for user update with Student account."""
        self.client.login(username=self.teacher.username,
                          password='1234')
        post = {'email': 'teacher_updated@test.com', 'first_name': 'Tim',
                'last_name': 'Teacher'}
        response = self.client.post(self.update_url, post)
        updated_teacher = SchoolUser.objects.get(
            username=self.teacher.username)
        self.assertEqual(updated_teacher.email, post['email'])
