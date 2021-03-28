from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.mail import mail_admins

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Layout, HTML


class ContactForm(forms.Form):
    name = forms.CharField(max_length=125)
    email = forms.EmailField()
    subject = forms.CharField(max_length=255)
    message = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = 'blog:contact'
        self.helper.layout = Layout(
            Div(
                Div(
                    'name', css_class='col-md-6'
                ),
                Div(
                    'email', css_class='col-md-6'
                ),
                Div(
                    'subject', css_class='col-md-12'
                ),

                Div(
                    'message', css_class='col-md-12'
                ),
                HTML(
                    """
                    <div class="col-xs-12 col-md-12 form-group">
                        <button class="btn btn-info pull-right" type="submit"><i class="fa fa-paper-plane-o"
                                                                                 aria-hidden="true"></i>
                            Submit
                        </button>
                    </div>
                    """
                ),
                css_class='row'
            )
        )
        self.fields['message'].widget.attrs['rows'] = 6
        self.fields['name'].widget.attrs['placeholder'] = _('name')
        self.fields['email'].widget.attrs['placeholder'] = _('email')
        self.fields['subject'].widget.attrs['placeholder'] = _('subject')
        self.fields['message'].widget.attrs['placeholder'] = _('message')

    def send(self):
        mail_admins(
            subject=self.cleaned_data.get('subject'),
            message=self.cleaned_data.get('message')
        )
