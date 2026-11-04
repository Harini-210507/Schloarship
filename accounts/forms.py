from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import StudentProfile


class StudentRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, label='First Name')
    last_name  = forms.CharField(max_length=50, required=True, label='Last Name')
    email      = forms.EmailField(required=True, label='Email Address')

    class Meta:
        model  = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username


class StudentLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))


class StudentProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name  = forms.CharField(max_length=50, required=True)
    email      = forms.EmailField(required=True)

    class Meta:
        model  = StudentProfile
        fields = ('phone', 'date_of_birth', 'address')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial  = user.last_name
            self.fields['email'].initial      = user.email
        self._user = user

    def save(self, commit=True):
        profile = super().save(commit=False)
        if self._user:
            self._user.first_name = self.cleaned_data['first_name']
            self._user.last_name  = self.cleaned_data['last_name']
            self._user.email      = self.cleaned_data['email']
            self._user.save()
        if commit:
            profile.save()
        return profile

