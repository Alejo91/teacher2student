from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

TYPE_USER = (
    ('teacher', _('Teacher')),
    ('student', _('Student')),
)

class SchoolUser(AbstractUser):
    """Custom user that can represent a Teacher or a Student"""
    # Type of User
    user_type = models.CharField(_('Type'), choices=TYPE_USER, max_length=20, default='student')

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_homework_url(self):
        if self.user_type == 'student':
            return reverse('homework:student_list_homework')
        else:
            return reverse('homework:list')

    def is_teacher(self):
        return self.user_type == 'teacher'

    def is_student(self):
        return self.user_type == 'student'

