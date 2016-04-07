from django.conf.urls import url
from users import views

urlpatterns = [
    # URL pattern for Teacher account creation view
    url(
        regex=r'^signup/teacher$',
        view=views.CreateTeacherView.as_view(),
        name='teacher_signup'
    ),
    # URL pattern for Student account creation view 
    url(
        regex=r'^signup/student$',
        view=views.CreateStudentView.as_view(),
        name='student_signup'
    ),
    # URL pattern for user Signin view 
    url(
        regex=r'^signin$',
        view=views.SigninView.as_view(),
        name='signin'
    ),
    # URL pattern for user Logout view 
    url(
        regex=r'^logout$',
        view=views.logout_view,
        name='logout'
    ),
    # URL pattern for Profile update view
    url(
        regex=r'^my_profile$',
        view=views.UserUpdateView.as_view(),
        name='profile'
    ),
]
