from homework.models import Homework, Answer
import floppyforms.__future__ as forms
from floppyforms.widgets import TextInput, HiddenInput, Textarea
from teacher2student.custom_widgets import DatePicker

class HomeworkCreateForm(forms.ModelForm):
    """."""

    class Meta:
        model = Homework
        fields = ('title', 'question', 'due_date', 'teacher')
        widgets = {
            'teacher': HiddenInput,
            'question': Textarea(attrs={
                'placeholder': 'Write the question for this homework.',
                'rows': 4}),
            'due_date': DatePicker(attrs={
                'placeholder': 'Select due date'}
            )
        }

class AnswerCreateForm(forms.ModelForm):
    """."""

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
