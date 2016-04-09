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

    def get_homework_url(self):
        if self.user_type == 'student':
            return reverse('homework:student_list_homework', kwargs={'pk': self.id})
        else:
            return reverse('homework:list')
