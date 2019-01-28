from django import forms
from crispy_forms.helper import FormHelper


class SearchForm(forms.Form):
    query = forms.CharField()
    error_css_class = "error alert alert-danger"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields["query"].label = ""
