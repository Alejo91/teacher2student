from django.shortcuts import render
from django.views.generic import CreateView, DetailView, FormView, UpdateView
from django.core.urlresolvers import reverse
import logging
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from users.models import SchoolUser
from users.forms import SignupForm, SigninForm, UserUpdateForm

logger = logging.getLogger(__name__)

# Create your views here.
class CreateUserBaseView(CreateView):
    """Base view for user creation."""
    model = SchoolUser
    form_class = SignupForm
    template_name = 'users/signup.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
            # Redirects to home page if user already logged in
            return HttpResponseRedirect(reverse('home'))
        return super(CreateUserBaseView, self).dispatch(
            request, *args, **kwargs)

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        user_type = form.cleaned_data['user_type']
        # Default username is email address
        username = email
        # Create new user
        user = SchoolUser(
            username=username, email=email, first_name=first_name,
            last_name=last_name, user_type=user_type
        )
        user.set_password(password)
        user.save()
        print(user)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
            else:
                logger.error("Disabled account")
        else:
            logger.error("Signup: Problem occured while logging in.")
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('home')


class CreateTeacherView(CreateUserBaseView):
    """View to create a new teacher.""" 
    def get_initial(self):
        initial = super(CreateTeacherView, self).get_initial()
        initial['user_type'] = 'teacher'
        initial['username'] = 'teacher'
        return initial

class CreateStudentView(CreateUserBaseView):
    """View to create a new student.""" 
    def get_initial(self):
        initial = super(CreateStudentView, self).get_initial()
        initial['user_type'] = 'student'
        initial['username'] = 'teacher'
        return initial

class SigninView(FormView):
    form_class = SigninForm
    template_name = 'users/signin.html'

    def get_context_data(self, **kwargs):
        context = super(SigninView, self).get_context_data(**kwargs)
        # Handle next page after login
        context['next'] = self.request.GET.get('next', None)
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect("/")
        return super(SigninView, self).get(request, args, kwargs)

    def form_valid(self, form):
        username_or_email = form.cleaned_data['username_or_email']
        password = form.cleaned_data['password']
        try:
            # Looks up user by username
            user = SchoolUser.objects.get(username=username_or_email)
        except:
            # Tries with email
            try:
                user = SchoolUser.objects.get(email=username_or_email)
            except:
                user = None

        if user:
            user = authenticate(username=user.username, password=password)
            if user is not None:
                if user.is_active:
                    login(self.request, user)
                    # Redirects to the original page
                    next = self.request.GET.get('next')
                    if next:
                        return HttpResponseRedirect(next)
                    # Ridirects to the profile edit page
                    return HttpResponseRedirect(reverse('home'))
                else:
                    # Returns a 'disabled account' error message.
                    msg = "Your account has been Disabled."
                    form._errors['__all__'] = form.error_class([msg])
                    return self.render_to_response(
                        self.get_context_data(form=form))

        msg = "Please enter a correct Username/Email and password."
        form._errors['__all__'] = form.error_class([msg])
        return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

def logout_view(request):
    """View for logout.""" 
    logout(request)
    return HttpResponseRedirect(reverse('home'))

class UserUpdateView(UpdateView):
    """View for User profile update.""" 
    model = SchoolUser
    form_class = UserUpdateForm
    template_name = 'users/profile.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserUpdateView, self).dispatch(
            request, *args, **kwargs)

    def get_object(self):
        self.object = self.request.user
        return self.object

    def get_success_url(self):
        return reverse('users:profile')
