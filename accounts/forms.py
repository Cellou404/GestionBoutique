from django.forms import widgets
from .models import Profile
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column



class UpdateProfileForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea(attrs={'name': 'bio', 'rows': 3}), required=False)
    class Meta:
        model = Profile
        fields = ['profile_picture', 'username', 'email', 'first_name', 'last_name', 'designation', 'address', 'bio']


class UpdateProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture',]