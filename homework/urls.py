from django.conf.urls import url
from homework import views

urlpatterns = [
    # URL pattern for Homework creation view
    url(
        regex=r'^new$',
        view=views.HomeworkCreateView.as_view(),
        name='create'
    ),
    # URL pattern for homework update view
    url(
        regex=r'^(?P<pk>\d+)/update$',
        view=views.HomeworkUpdateView.as_view(),
        name='update'
    ),
    # URL pattern for Teacher account creation view
    url(
        regex=r'^all$',
        view=views.HomeworkListView.as_view(),
        name='list'
    ),
    # URL pattern for choosing new assignees
    url(
        regex=r'^(?P<pk>\d+)/assign$',
        view=views.homework_assign_view,
        name='assign_student_list'
    ),
    # URL pattern for adding assignment
    url(
        regex=r'^student/add$',
        view=views.homework_student_add,
        name='add_student'
    ),
    # URL pattern for removing assignment
    url(
        regex=r'^student/remove$',
        view=views.homework_student_remove,
        name='remove_student'
    ),
    # URL pattern for all answers for a student
    url(
        regex=r'^(?P<pk>\d+)/student/(?P<student>\d+)$',
        view=views.HomeworkStudentAnswersView.as_view(),
        name='homework_student_list'
    ),
    # URL pattern for list of student's homework
    url(
        regex=r'^student/(?P<pk>\d+)/all$',
        view=views.StudentHomeworkListView.as_view(),
        name='student_list_homework'
    ),
    # URL pattern for new student's answer
    url(
        regex=r'^(?P<pk>\d+)/answer/new$',
        view=views.AnswerCreateView.as_view(),
        name='new_answer'
    ),
]
