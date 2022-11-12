from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from newspaper.models import Redactor, Newspaper


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Username", "class": "form-control"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-control"}
        )
    )


class RedactorCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Redactor
        fields = UserCreationForm.Meta.fields + (
            "years_of_experience",
            "first_name",
            "last_name",
        )

    def clean_years_of_experience(self):
        data = self.cleaned_data["years_of_experience"]
        if data < 0 or data > 80:
            raise ValidationError(
                "Ensure that the years of experience is between 0 and 80"
            )

        return data


class RedactorUpdateForm(forms.ModelForm):
    class Meta:
        model = Redactor
        fields = ("years_of_experience", "first_name", "last_name")

    def clean_years_of_experience(self):
        data = self.cleaned_data["years_of_experience"]
        if data < 0 or data > 80:
            raise ValidationError(
                "Ensure that the years of experience is between 0 and 80"
            )

        return data


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
        widget=forms.TextInput(attrs={"placeholder": "Search by username"}),
    )


class NewspaperSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by title"}),
    )


class TopicSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
    )
