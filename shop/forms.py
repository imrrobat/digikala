from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django import forms
from .models import Profile

class UserInfoForm(forms.ModelForm):
    phone = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone'}),
        required=False,
        
    )
    address1 = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address1'}),
        required=False,
      
    )
    address2 = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address2'}),
        required=False,
      
    )
    city = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}),
        required=False,
      
    )
    state = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}),
        required=False,
      
    )
    zipcode = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'ZipCode'}),
        required=False,
      
    )
    country = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country'}),
        required=False,
      
    )
    
    class Meta:
        model = Profile
        fields = ('phone', 'address1', 'address2','city','state','zipcode','country')


class UpdatePasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'name':'password',
                'type':'password',
                'placeholder':'رمز بالای 8 کاراکتر را وارد کنید'
            }
        )
    )
    new_password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'name':'password',
                'type':'password',
                'placeholder':'دوباره رمز خود را وارد کنید'
            }
        )
    )
    class Meta:
        model = User
        fields = ['new_password1','new_password2']

class UpdateUserForm(UserChangeForm):
    password = None
    first_name = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'نام خود را وارد کنید'})
        ,required=False
    )
    last_name = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'نام خانوادگی خود را وارد کنید'})
        ,required=False
    )
    email = forms.EmailField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'ایمیل خود را وارد کنید'})
        ,required=False
    )
    username = forms.CharField(
        label="",
        max_length=20,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'نام کاربری'})
    )
    class Meta:
        model = User
        fields = ('first_name','last_name','email','username')
    


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'نام خود را وارد کنید'})
    )
    last_name = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'نام خانوادگی خود را وارد کنید'})
    )
    email = forms.EmailField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'ایمیل خود را وارد کنید'})
    )
    username = forms.CharField(
        label="",
        max_length=20,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'نام کاربری'})
    )
    password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'name':'password',
                'type':'password',
                'placeholder':'رمز بالای 8 کاراکتر را وارد کنید'
            }
        )
    )
    password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'name':'password',
                'type':'password',
                'placeholder':'دوباره رمز خود را وارد کنید'
            }
        )
    )
    
    class Meta:
        model = User
        fields = ('first_name','last_name','email','username','password1','password2')
    