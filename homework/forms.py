from homework.models import Homework, Answer
import floppyforms.__future__ as forms
from floppyforms.widgets import TextInput, HiddenInput, Textarea, DateInput


class HomeworkCreateForm(forms.ModelForm):
    """Form for Homework creation and update."""

    class Meta:
        model = Homework
        fields = ('title', 'question', 'due_date', 'teacher')
        widgets = {
            'teacher': HiddenInput,
            'question': Textarea(attrs={
                'placeholder': 'Write the question for this homework.',
                'rows': 4}),
            'due_date': DateInput
        }

class AnswerCreateForm(forms.ModelForm):
    """Form for Answer creation and update."""

    class Meta:
        model = Answer
        fields = ('description', 'student', 'homework')
        widgets = {
            'student': HiddenInput,
            'homework': HiddenInput,
            'description': Textarea(attrs={
                'placeholder': 'Write your answer.',
                'rows': 4}),
        }
