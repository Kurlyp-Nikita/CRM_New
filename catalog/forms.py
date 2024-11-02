from django import forms
from .models import Lead, Client, Team


class AddleadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ('name', 'email', 'description', 'priority', 'status',)


class AddClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'email', 'description',)


class AddTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name',)
