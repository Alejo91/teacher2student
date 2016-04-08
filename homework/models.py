from django.db import models
from django.utils.translation import ugettext_lazy as _
from users.models import SchoolUser

class Homework(models.Model):
    title = models.CharField(_("Title"), max_length=200)
    question = models.CharField(_("Question"), max_length=200)
    teacher = models.ForeignKey(
        SchoolUser, verbose_name=_("Teacher"))
    student = models.ManyToManyField(
        SchoolUser, verbose_name=_("Students"), 
        related_name="assigned_homeworks", blank=True)
    due_date = models.DateField(_("Due date"))
    pub_date = models.DateTimeField(auto_now_add=True)

class Answer(models.Model):
    description = models.CharField(_("Answer"), max_length=500)
    student = models.ForeignKey(
        SchoolUser, verbose_name=_("Student"))
    homework = models.ForeignKey(
        Homework, verbose_name=_("Student"))
    pub_date = models.DateTimeField(auto_now_add=True)

