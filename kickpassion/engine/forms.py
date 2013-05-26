from django import forms
from django.forms import ModelForm, Textarea, TextInput, Select

from kickpassion.engine.models import Passion, Profile, Meeting, FIleInput

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user','disciples','counselors','teach_passions')
        widgets = {
        'picture' : FileInput(attrs={'placeholder':'Picture'}),
        'location' : TextInput(attrs={'placeholder':'Location'}),
        'bio' : TextInput(attrs={'placeholder':'Biography'}),
        }

class PassionForm(ModelForm):
    class Meta:
        model = Passion
        exclude = ('owner','counselors')
        widgets = {
        'category' : Select(attrs={'placeholder':'Category'}),
        'name' : TextInput(attrs={'placeholder':'Name'}),
        'video_url' : TextInput(attrs={'placeholder':'Video url'}),
        'pictures' : FileInput(attrs={'placeholder':'Pictures'}),
        'description' : TextInput(attrs={'placeholder':'Description'}),
        'location' : TextInput(attrs={'placeholder':'Location'}),
        }

class MeetingForm(ModelForm):
    class Meta:
        model = Meeting
        exclude = ('passion','counselor','disciples')
        widgets = {
        'description' : TextInput(attrs={'placeholder':'Description'}),
        }