from __future__ import unicode_literals
from future.builtins import int

from collections import defaultdict

from django.core.urlresolvers import reverse
from django.template.defaultfilters import linebreaksbr, urlize

from mezzanine import template
from mezzanine.conf import settings
from mezzanine.generic.forms import ThreadedCommentForm
from mezzanine.generic.models import ThreadedComment
from mezzanine.utils.importing import import_dotted_path

from drum.links.models import Link, WaveSurfComment

register = template.Library()


@register.inclusion_tag("generic/includes/comments.html", takes_context=True)
def comments_for(context, obj):
    """
    Provides a generic context variable name for the object that
    comments are being rendered for.
    """

    form = ThreadedCommentForm(context["request"], obj)
    try:
        context["posted_comment_form"]
    except KeyError:
        context["posted_comment_form"] = form
    context["unposted_comment_form"] = form
    context["comment_url"] = reverse("comment")
    context["object_for_comments"] = obj
    return context


@register.inclusion_tag("generic/includes/comment.html", takes_context=True)
def comment_thread(context, parent):
    """
    Return a list of child comments for the given parent, storing all
    comments in a dict in the context when first called, using parents
    as keys for retrieval on subsequent recursive calls from the
    comments template.
    """
    parent_comments = WaveSurfComment.objects.for_model(Link).filter(object_pk=parent.id)
    if len(parent_comments) != 0:
        context["comments_for_thread"] = parent_comments
    else:
        context["no_comments"] = 'no_comments'
    return context


@register.inclusion_tag("admin/includes/recent_comments.html",
                        takes_context=True)
def recent_comments(context):
    """
    Dashboard widget for displaying recent comments.
    """
    latest = context["settings"].COMMENTS_NUM_LATEST
    comments = ThreadedComment.objects.all().select_related("user")
    context["comments"] = comments.order_by("-id")[:latest]
    return context


@register.filter
def comment_filter(comment_text):
    """
    Passed comment text to be rendered through the function defined
    by the ``COMMENT_FILTER`` setting. If no function is defined
    (the default), Django's ``linebreaksbr`` and ``urlize`` filters
    are used.
    """
    filter_func = settings.COMMENT_FILTER
    if not filter_func:
        def filter_func(s):
            return linebreaksbr(urlize(s, autoescape=True), autoescape=True)
    elif not callable(filter_func):
        filter_func = import_dotted_path(filter_func)
    return filter_func(comment_text)
