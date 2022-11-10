from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from newspaper.models import Redactor, Newspaper


class RedactorCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Redactor
        fields = UserCreationForm.Meta.fields + (
            "years_of_experience",
            "first_name",
            "last_name",
        )

    def clean_license_number(self):
        return validate_years_of_experience(self.cleaned_data["years_of_experience"])


class RedactorYearsUpdateForm(forms.ModelForm):
    class Meta:
        model = Redactor
        fields = ("years_of_experience",)

    def clean_license_number(self):
        return validate_years_of_experience(self.cleaned_data["years_of_experience"])


def validate_years_of_experience(years_of_experience):
    if not 0 < years_of_experience < 80:
        raise ValidationError(
            "Ensure that the years of experience is between 0 and 80"
        )


class DateInput(forms.DateInput):
    input_type = "date"


class NewspaperForm(forms.ModelForm):
    redactor = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    published_date = forms.DateField(widget=DateInput)

    class Meta:
        model = Newspaper
        fields = "__all__"


class RedactorSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username"})
    )


class NewspaperSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by title"})
    )


class TopicSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"})
    )
