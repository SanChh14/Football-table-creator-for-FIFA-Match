from django.forms import ModelForm
from . import models

class Team(ModelForm):
    class Meta:
        model = models.Team
        fields = ['name']

class Fixtures(ModelForm):
    class Meta:
        model = models.Fixtures
        fields = ['t1g', 't2g']
