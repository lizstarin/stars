from django import forms
from django.core.validators import RegexValidator

class RepoForm(forms.Form):
    repo_one = forms.URLField(label='repo one', validators=[RegexValidator(r'^https://github.com/[\w~.-]+\/[\w~.-]+$', 'Enter a valid repository.')])
    repo_two = forms.URLField(label='repo two', validators=[RegexValidator(r'^https://github.com/[\w~.-]+\/[\w~.-]+$', 'Enter a valid repository.')])

