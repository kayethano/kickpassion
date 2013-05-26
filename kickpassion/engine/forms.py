from django import forms
from django.forms import ModelForm, Textarea, TextInput, Select, FileInput

from kickpassion.engine.models import Passion, Profile, Meeting

PASSION_CHOICES = (

    ('Art','Art'),
    ('Sports','Sports'),
    ('Science', 'Science'),
    ('Technology','Technology'),

    )

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user','disciples','counselors','teach_passions')
        widgets = {
        'picture' : FileInput(attrs={'placeholder':'Picture'}),
        'location' : TextInput(attrs={'placeholder':'Location'}),
        'bio' : TextInput(attrs={'placeholder':'Biography'}),
        }


class PassionForm(forms.Form):
    category = forms.ChoiceField(
        widget = forms.Select(attrs={'class':'input-text', 'placeholder' : 'Select Category'}),
        choices = PASSION_CHOICES)
    name = forms.CharField(
        widget = forms.TextInput(attrs={'class':'input-text', 'placeholder' : 'Surrealism Art'}))
    video_url = forms.URLField(
        widget = forms.TextInput(attrs={'class':'input-text', 'placeholder' : 'http://www.youtube.com/watch?v=f7SSkVpM4lE'}))
    picture1 = forms.ImageField(
        widget = forms.ClearableFileInput(attrs = {'class' : 'input-file', 
            'onChange' : "readURL(this,'image1')"}))
    picture2 = forms.ImageField(required=False,
        widget = forms.ClearableFileInput(attrs = {'class' : 'input-file', 
            'onChange' : "readURL(this,'image2')"}))
    picture3 = forms.ImageField(required=False, 
        widget = forms.ClearableFileInput(attrs = {'class' : 'input-file', 
            'onChange' : "readURL(this,'image3')"}))
    picture4 = forms.ImageField(required=False, 
        widget = forms.ClearableFileInput(attrs = {'class' : 'input-file', 
            'onChange' : "readURL(this,'image4')"}))
    picture5 = forms.ImageField(required=False, 
        widget = forms.ClearableFileInput(attrs = {'class' : 'input-file', 
            'onChange' : "readURL(this,'image5')"}))
    description = forms.CharField(
        widget = forms.Textarea(attrs = {'class':'input-text', 'placeholder' : 'Description'}))
    location = forms.CharField(
        widget = forms.TextInput(attrs={'class':'input-text', 'placeholder' : 'Location'}))


class MeetingForm(ModelForm):
    class Meta:
        model = Meeting
        exclude = ('passion','counselor','disciples')
        widgets = {
        'description' : TextInput(attrs={'placeholder':'Description'}),
        }