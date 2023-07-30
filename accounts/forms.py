from django import forms

from accounts.validators import allow_only_image_validator
from .models import User, UserProfile

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'username', 'password']

    
    def clean(self):
        cleaned_data = super(UserRegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Password doesn't match.")
            

class User_Profile_Form(forms.ModelForm):
    address = forms.CharField(widget= forms.TextInput(attrs={'placeholder' : 'start typing...', 'required' : 'required'}))
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class': 'border-btn input-btn'}), validators=[allow_only_image_validator])
    
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'address', 'city','country', 'state', 'pin_code']

    def __init__(self, *args, **kwargs):
        super(User_Profile_Form, self).__init__(*args, **kwargs)
        for field in self.fields:
            if not field == 'profile_picture':
                self.fields[field].widget.attrs['class'] = 'form-control'

    


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number']


    def __init__(self, *args, **kwargs):
        super(UserInfoForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'