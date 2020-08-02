from django import forms
from django.db.models import Q
from hrm import models
from officeStructure import models as office_models
from userManagement import models as user_models
from helper import choices as choice_helper


class TrainingForm(forms.ModelForm):
    def __init__(self, current_branch, *args, **kwargs):
        print(current_branch)
        super(TrainingForm, self).__init__(*args, **kwargs)
        self.fields['employees'].queryset = self.fields['employees'].queryset.filter(branch=current_branch, is_superuser=False)
        

    start_date = forms.DateField(widget=forms.DateInput(
        attrs={"id": "datepicker", "autocomplete": "off"}), required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={"rows": "3"}), required=False)
    branch = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(
        attrs={"multiple": "multiple", "data-placeholder": "Select branches"}), queryset=office_models.Branches.objects.all(), help_text="Show trainings in which branch/branches?", required=False)
    branch_accepted = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(
        attrs={"multiple": "multiple", "data-placeholder": "Select branches"}), queryset=office_models.Branches.objects.all(), help_text="Which branch has accepted for this training?", required=False)
    completed = forms.ChoiceField(choices=choice_helper.yes_no, required=False)

    class Meta:
        model = models.Training
        fields = '__all__'

    