from __future__ import unicode_literals

from django.conf import settings
from django.contrib import admin
from django.db import connection

from mezzanine.core.admin import DisplayableAdmin
from drum.links.models import Link
from django.contrib.comments import *
from django_select2 import *
from django import forms


class CommentsWidget(AutoHeavySelect2MultipleWidget):
    def render(self, name, value, attrs=None, choices=()):
        params = attrs
        params['control'] = super(CommentsWidget, self).render(name, value, attrs, choices)
        html = render_to_string("widget_many_to_many.html", attrs)
        print 'COMMENT'
        return mark_safe(html)


class CommentsChoices(AutoModelSelect2MultipleField):
    queryset = Comment.objects
    search_fields = ['comment__icontains', ]

    widget = CommentsWidget


class LinkForm(forms.ModelForm):
    comments = CommentsChoices

    class Meta:
        model = Comment
        fields = ('comment',)

class LinkAdmin(DisplayableAdmin):

    list_display = ("id", "title", "link", "status", "publish_date",
                    "user", "comments_count", "rating_sum")
    list_display_links = ("id",)
    list_editable = ("title", "link", "status")
    list_filter = ("status", "user__username")
    search_fields = ("title", "link", "user__username", "user__email")
    ordering = ("-publish_date",)

    fieldsets = (
        (None, {
            "fields": ("title", "link", "status", "publish_date", "user"),
        }),
    )


def delete_keywords(modeladmin, request, queryset):
    ids = ",".join(map(str, queryset.values_list("id", flat=True)))
    cursor = connection.cursor()
    cursor.execute("DELETE FROM generic_assignedkeyword "
                   "WHERE keyword_id IN (%s);" % ids)
    cursor.execute("DELETE FROM generic_keyword WHERE id IN (%s);" % ids)


class KeywordAdmin(admin.ModelAdmin):

    ordering = ["title"]
    list_display = ["id", "title", "slug"]
    list_editable = ["title", "slug"]
    actions = [delete_keywords]

    class Media:
        css = {"all": ["css/keywords.css"]}

    def get_actions(self, request):
        actions = super(KeywordAdmin, self).get_actions(request)
        actions.pop("delete_selected")
        return actions


admin.site.register(Link, LinkAdmin)

if getattr(settings, "AUTO_TAG", False):
    from mezzanine.generic.models import Keyword
    admin.site.register(Keyword, KeywordAdmin)
