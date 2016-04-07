from users.models import SchoolUser
import floppyforms.__future__ as forms
from floppyforms.widgets import PasswordInput, TextInput, HiddenInput

class SignupForm(forms.ModelForm):
    """Form for signing up new users."""

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta:
        model = SchoolUser
        fields = ('email', 'first_name', 'last_name', 'password', 'user_type')
        widgets = {
            'password': PasswordInput(),
            'user_type': HiddenInput(),
        }

    def clean_email(self):
        """Make sure the email doesn't exist already."""
        data = self.cleaned_data['email']
        if SchoolUser.objects.filter(email=data).exists():
            raise forms.ValidationError("This email already used")
        return data

class SigninForm(forms.ModelForm):
    """Form for signing in the user."""
    username_or_email = forms.CharField(
        max_length=250,
        label= "Email",
        required=True,
        widget=TextInput(attrs={
            'placeholder': "Email",
            'autocapitalize': "none",
            'autocorrect': "off"})
    )

    class Meta:
        model = SchoolUser
        fields = ('username_or_email', 'password')
        widgets = {
            'password': PasswordInput(attrs={'placeholder': "Password"}),
        }

    def clean_username_or_email(self):
        username_or_email = self.cleaned_data['username_or_email'].strip()
        print(username_or_email)
        if not username_or_email:
            raise forms.ValidationError('Please input valid username or email.')
        return username_or_email

class UserUpdateForm(forms.ModelForm):
    """Form for updating user info."""

    class Meta:
        model = SchoolUser
        fields = ('email', 'first_name', 'last_name')
