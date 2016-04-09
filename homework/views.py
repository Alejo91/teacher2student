from datetime import datetime, date

from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.views.generic import CreateView, UpdateView, ListView

from .models import Homework, Answer
from users.models import SchoolUser 
from .forms import HomeworkCreateForm, AnswerCreateForm


########## Helper functions views permission ##########
def check_teacher_user(request):
    if request.user.user_type != 'teacher':
        raise PermissionDenied
    return request

def check_student_user(request):
    if request.user.user_type != 'student':
        raise PermissionDenied
    return request

########## Teacher Views ##########
class HomeworkCreateView(CreateView):
    """Homework creation."""
    model = Homework
    form_class = HomeworkCreateForm
    template_name = 'homework/create.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        request = check_teacher_user(request)
        return super(HomeworkCreateView, self).dispatch(
            request, *args, **kwargs)

    def get_initial(self):
        """Add initial value to set current user as the teacher."""
        initial = super(HomeworkCreateView, self).get_initial()
        initial['teacher'] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        context = super(HomeworkCreateView, self).get_context_data(**kwargs)
        context['default_due_date'] = datetime.today()
        return context

    def get_success_url(self):
        return reverse('homework:list')


class HomeworkUpdateView(UpdateView):
    """Homework update."""
    model = Homework
    form_class = HomeworkCreateForm
    template_name = 'homework/create.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        request = check_teacher_user(request)
        return super(HomeworkUpdateView, self).dispatch(
            request, *args, **kwargs)

    def get_initial(self):
        """Add initial value to set current user as the teacher."""
        initial = super(HomeworkUpdateView, self).get_initial()
        initial['teacher'] = self.request.user
        return initial

    def get_success_url(self):
        return reverse('homework:list')


class HomeworkListView(ListView):
    """Teacher's homework List."""
    model = Homework
    template_name = 'homework/list.html'
    paginate_by = 10

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        request = check_teacher_user(request)
        return super(HomeworkListView, self).dispatch(
            request, *args, **kwargs)



@login_required
def homework_assign_view(request, pk):
    """Teacher can assign homework to students."""
    request = check_teacher_user(request)
    homework = get_object_or_404(Homework, id=int(pk))
    # Check that the homework belong to the teacher
    if homework.teacher != request.user:
        raise PermissionDenied
    students = SchoolUser.objects.filter(user_type='student')
    context_data = {
        'teacher': request.user,
        'homework': homework,
        'students': students,
        'request': request
    }
    return render_to_response('homework/assign_students.html', context_data)


@login_required
def homework_student(request):
    """
    Helper function for Assign/Remove homework to/from a student.
    """
    if request.method == 'POST':
        try:
            homework_id = request.POST.get('homework_id')
            request.homework = Homework.objects.get(id=int(homework_id))
            student_id = request.POST.get('student_id')
            request.student = SchoolUser.objects.get(id=int(student_id))
        except KeyError:
            print("Bad POST data for Assign/Remove student.")
        if request.student.user_type == 'student':
            return request
    raise Http404


def homework_student_add(request):
    """Assign homework to student."""
    request = homework_student(request) 
    request.homework.student.add(request.student)
    return HttpResponse("Added")


def homework_student_remove(request):
    """Remove homework from student."""
    request = homework_student(request) 
    request.homework.student.remove(request.student)
    return HttpResponse("Removed")
    

class HomeworkStudentAnswersView(ListView):
    """All submission versions for a student for a homework."""
    model = Answer
    template_name = 'homework/answer_list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        request = check_teacher_user(request)
        self.request.homework = get_object_or_404(
            Homework, id=int(self.kwargs['pk']))
        # Check that the homework belong to the teacher
        if homework.teacher != request.user:
            raise PermissionDenied
        return super(HomeworkStudentAnswersView, self).dispatch(
            request, *args, **kwargs)

    def get_queryset(self):
        self.request.student = get_object_or_404(
            SchoolUser, id=self.kwargs['student'])
        answers = Answer.objects.filter(
            homework=self.request.homework, 
            student=self.request.student
        )
        return answers 

class HomeworkLatestAnswersView(ListView):
    """Teacher can see a list of latest submissions for a homework"""
    pass


########## Students Views ##########
class StudentHomeworkListView(ListView):
    """List all the student's homework."""
    model = Homework
    template_name = 'homework/student_list_homework.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        request = check_student_user(request)
        return super(StudentHomeworkListView, self).dispatch(
            request, *args, **kwargs)

    def get_queryset(self):
        homeworks = Homework.objects.filter(
            student=self.request.user)
        return homeworks

    def get_context_data(self, **kwargs):
        context = super(StudentHomeworkListView, self).get_context_data(**kwargs)
        context['today'] = date.today()
        return context


class AnswerCreateView(CreateView):
    """Student submit a new answer."""
    model = Answer
    form_class = AnswerCreateForm
    template_name = 'homework/answer_create.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        request = check_student_user(request)
        return super(AnswerCreateView, self).dispatch(
            request, *args, **kwargs)

    def get_initial(self):
        """Add initial value for homework and student."""
        initial = super(AnswerCreateView, self).get_initial()
        self.request.homework = get_object_or_404(
            Homework, id=int(self.kwargs['pk']))
        initial['homework'] = self.request.homework
        initial['student'] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        context = super(AnswerCreateView, self).get_context_data(**kwargs)
        context['homework'] = self.request.homework
        # Check if student had previous answer and get latest
        answers = Answer.objects.filter(
            homework=self.request.homework,
            student=self.request.user
        )
        if answers:
            # Latest answer
            context['last_answer'] = answers.order_by('-pub_date')[0]
        return context

    def get_success_url(self):
        return reverse('homework:list')
