from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
        min_length=8,
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
        min_length=8,
        label="confirm Password"
    )
    class Meta:
        model = User
        fields = ['email', 'name', 'password']
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control','id':'formGroupExampleInput', 'placeholder': 'Enter Email'}),
            'name': forms.TextInput(attrs={'class': 'form-control','id':'formGroupExampleInput', 'placeholder': 'Enter Name'}),
            'password': forms.TextInput(attrs={'class': 'form-control','id':'formGroupExampleInput','type': 'password'}),
            'confirm_password': forms.TextInput(attrs={'class': 'form-control','id':'formGroupExampleInput','type': 'password'}),
            
        }

        def clean(Self):
            cleaned_data = super().clean()
            password = cleaned_data.get('password')
            confirm_pass = cleaned_data.get('confirm_password')
            if password != confirm_pass:
                raise forms.ValidationError('Password does not match')
            return cleaned_data
        


class UserLoginForm(forms.Form):
    """Login form"""
    email = forms.EmailField(
        label='Email', 
        max_length=255,
        widget=forms.EmailInput(attrs={'class': 'form-control','id':'formGroupExampleInput'})
    )  
    password = forms.CharField(label='Password', 
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control','id':'formGroupExampleInput'})
                            )
                               
