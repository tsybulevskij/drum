from django import forms
from django.conf import settings
from django.forms.models import modelform_factory
from django.forms import ValidationError
from mezzanine.generic.forms import ThreadedCommentForm
from drum.links.models import Link

BaseLinkForm = modelform_factory(Link, fields=["title", "link", "description"])


class LinkForm(BaseLinkForm):
    def clean(self):
        link = self.cleaned_data.get("link", None)
        description = self.cleaned_data.get("description", None)
        if not link and not description:
            raise ValidationError("Either a link or description is required")
        return self.cleaned_data


class ExtendedCommentForm(ThreadedCommentForm):
    start = forms.FloatField(label="Start", help_text="optional",
                             required=False)
    end = forms.FloatField(label="End", help_text="optional",
                           required=False)
    cookie_fields = ("name", "email", "url", "start", "end",)
