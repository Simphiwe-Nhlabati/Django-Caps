# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegisterForm(UserCreationForm):
    
    USER_CHOICES = [
        ('reader', 'Reader'),
        ('editor', 'Editor'),
        ('journalist', 'Journalist'),
    ]
    
    position = forms.ChoiceField(
        choices=USER_CHOICES,
        required=True
    )
    
    # password = forms.CharField(widget=forms.PasswordInput)
    # password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'first_name',
                  'last_name',
                  'password1',
                  'password2'
                  ]
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError("Username is required.")
        
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username
    
    # def clean(self):
    #     cleaned_data = super().clean()
    #     password = cleaned_data.get("password")
    #     password2 = cleaned_data.get("password2")

    #     if password and password2 and password != password2:
    #         self.add_error('password2', "Passwords don't match.")
    #     return cleaned_data
        
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Enter your username'
        self.fields['username'].label = 'Username'
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
        
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email'
        self.fields['email'].label = 'Email'
        self.fields['email'].help_text = '<span class="form-text text-muted"><small>Required. Enter a valid email address.</small></span>'
        
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter your first name'
        self.fields['first_name'].label = 'First Name'
        
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter your last name'
        self.fields['last_name'].label = 'Last Name'
        
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter your password'
        self.fields['password1'].label = 'Password'
        self.fields['password1'].help_text = '<span class="form-text text-muted"><small>Required. 8 characters or more. Letters, digits and @/./+/-/_ only.</small></span>'
        
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm your password'
        self.fields['password2'].label = 'Confirm Password'
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>The password should match each other.</small></span>'
        
        self.fields['position'].widget.attrs['class'] = 'form-control'
        self.fields['position'].widget.attrs['placeholder'] = 'Select your position'
        self.fields['position'].label = 'Position'
        self.fields['position'].help_text = '<span class="form-text text-muted"><small>Select your option.</small></span>'
        
        
class UserRestPassword(PasswordResetForm):
    class Meta(PasswordResetForm):
        model = User
        fields = ('email',)