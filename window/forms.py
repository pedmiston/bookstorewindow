from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field
from crispy_forms.bootstrap import StrictButton


class SearchForm(forms.Form):
    query = forms.CharField()
    error_css_class = "error alert alert-danger"


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields["query"].label = ""

        self.helper.form_class = 'form-inline'
        self.helper.layout = Layout(
            Div(
                Field("query", css_class="col mx-1"),
                StrictButton("Search", css_class="col btn btn-secondary ml-2", type="submit"),
                css_class="form-row"
            )
        )
