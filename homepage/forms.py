from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django import forms


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, help_text='Required.') #Not in original code
    email = forms.EmailField(label="", required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label="", required=True, max_length=60, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", required=True, max_length=60, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))


    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	

class ProfileForm(forms.ModelForm):
    phone = forms.CharField(label="", required=False, max_length=15, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone'}))
    city = forms.CharField(label="", required=True, max_length=30, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}))
    state = forms.CharField(label="", required=True, max_length=30, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}))
    zip = forms.CharField(label="", required=False, max_length=10, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zip'}))
    country = forms.CharField(label="", required=True, max_length=30, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country'}))
    gender = forms.CharField(label="", required=False, max_length=30, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Gender'}))
    image = forms.ImageField(label="", required=False, widget=forms.FileInput(attrs={'class':'form-control'}))

    class Meta:
        model = Profile
        fields = ('phone', 'city', 'state', 'zip', 'country', 'gender', 'image')