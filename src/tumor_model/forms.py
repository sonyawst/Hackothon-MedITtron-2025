# forms.py
from django import forms
from .models import Patients, PathologicalProfiles

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patients
        fields = ['age', 'gender', 'menopausal_status', 'family_history']

class PathologicalProfileForm(forms.ModelForm):
    class Meta:
        model = PathologicalProfiles
        fields = ['molecular_subtype', 'er_status', 'pr_status', 'her2_status']