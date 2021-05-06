from django import forms
from django.utils.translation import ugettext_lazy as _

from django_comments.forms import CommentForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Hidden, Submit

from . import get_model

import django_comments


class MyCommentForm(CommentForm):
    parent = forms.IntegerField(required=False, widget=forms.HiddenInput)

    def __init__(self, target_object, parent=None, data=None, initial=None, **kwargs):
        self.parent = parent
        if initial is None:
            initial = {}
        initial.update({'parent': self.parent})
        super(MyCommentForm, self).__init__(target_object, data=data, initial=initial, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_action = django_comments.get_form_target()
        self.helper.layout = Layout(
            Div(
                'honeypot',
                'parent',
                'content_type',
                'object_pk',
                'timestamp',
                'security_hash',
                Hidden('next', '{% url "comments:comment_success" %}'),
                Div(
                    'name', css_class='col-md-4'
                ),
                Div(
                    'email', css_class='col-md-4'
                ),
                Div(
                    'url', css_class='col-md-4'
                ),
                Div(
                    'comment', css_class='col-md-12'
                ),
                css_class='row'
            )
        )
        self.helper.add_input(Submit('submit', '发表评论', css_class='btn-sm pull-xs-right'))
        self.fields['comment'].widget.attrs['rows'] = 6
        self.fields['comment'].label = '评论'
        self.fields['name'].label = '名字'
        self.fields['url'].label = '网址'

    def get_comment_model(self):
        return get_model()

    def get_comment_create_data(self):
        d = super(MyCommentForm, self).get_comment_create_data()
        d['parent_id'] = self.cleaned_data['parent']
        return d
