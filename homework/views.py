from datetime import datetime
from django.shortcuts import render, render_to_response, get_object_or_404
from django.views.generic import CreateView, UpdateView, ListView
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Homework, Answer
from users.models import SchoolUser 
from .forms import HomeworkCreateForm, AnswerCreateForm


########## Teacher Views ##########
class HomeworkCreateView(CreateView):
    """Homework contains a title, a question and a due date."""
    model = Homework
    form_class = HomeworkCreateForm
    template_name = 'homework/create.html'

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
    """
    Homework contains a title, a question and a due date.
    Teacher can assign a homework to multiple students
    """
    model = Homework
    form_class = HomeworkCreateForm
    template_name = 'homework/create.html'

    def get_initial(self):
        """Add initial value to set current user as the teacher."""
        initial = super(HomeworkUpdateView, self).get_initial()
        initial['teacher'] = self.request.user
        return initial

    def get_success_url(self):
        return reverse('homework:list')

    def form_invalid(self, form):
        print(form.errors)
        return super(HomeworkUpdateView, self).form_invalid(form)


class HomeworkListView(ListView):
    """
    Homework contains a title, a question and a due date.
    Teacher can assign a homework to multiple students
    """
    model = Homework
    template_name = 'homework/list.html'
    paginate_by = 10


def homework_assign_view(request, pk):
    homework = Homework.objects.get(id=int(pk))
    students = SchoolUser.objects.filter(user_type='student')
    print(students)
    context_data = {
        'teacher': request.user,
        'homework': homework,
        'students': students,
    }
    return render_to_response('homework/assign_students.html', context_data)


def homework_student(request):
    """Helper function for Add/Remove student's homework."""
    if self.request.method == 'POST':
        try:
            homework_id = request.POST.get('homework_id')
            request.homework = Homework.objects.get(id=int(homework_id))
            student_id = request.POST.get('student_id')
            request.student = SchoolUser.objects.get(id=int(student_id))
        except KeyError:
            print("Bad POST data for Add/Remove student.")
        if student.user_type == 'student':
            return request
    raise Http404


def homework_student_add(request, pk, student):
    """Assign new homework to student."""
    request = homework_student(request, pk, student) 
    request.homework.student.add(request.student)
    return HttpResponse("Added")


def homework_student_remove(request, pk, student):
    """Remove homework assignment for specified student."""
    request = homework_student(request, pk, student) 
    request.homework.student.remove(request.student)
    return HttpResponse("Removed")
    

class HomeworkStudentAnswersView(ListView):
    """All submission versions for a student for a homework."""

    def get_queryset(self):
        self.request.homework = get_object_or_404(
            Homework, id=int(self.kwargs['pk']))
        self.request.student = get_object_or_404(
            Student, id=self.kwargs['student'])
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
    template_name = 'homework/student_list.html'

    def get_queryset(self):
        homeworks = get_object_or_404(
            Homework, id=self.request.user.id)
        return homeworks

class AnswerCreateView(CreateView):
    """View to submit an answer."""
    model = Answer
    form_class = AnswerCreateForm
    template_name = 'homework/answer_create.html'

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
