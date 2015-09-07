from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from drum.links.views import LinkList, LinkCreate, LinkDetail, TagList, WaveSurfCommentList


urlpatterns = patterns("",
    url("^$",
        LinkList.as_view(),
        name="home"),
    url("^newest/$",
        LinkList.as_view(), {"by_score": False},
        name="link_list_latest"),
    url("^comments/$",
        WaveSurfCommentList.as_view(), {"by_score": False},
        name="comment_list_latest"),
    url("^best/$",
        WaveSurfCommentList.as_view(),
        name="comment_list_best"),
    url("^link/create/$",
        login_required(LinkCreate.as_view()),
        name="link_create"),
    url("^link/(?P<slug>.*)/$",
        LinkDetail.as_view(),
        name="link_detail"),
    url("^users/(?P<username>.*)/links/$",
        LinkList.as_view(), {"by_score": False},
        name="link_list_user"),
    url("^users/(?P<username>.*)/comments/$",
        WaveSurfCommentList.as_view(), {"by_score": False},
        name="comment_list_user"),
    url("^tags/$",
        TagList.as_view(),
        name="tag_list"),
    url("^tags/(?P<tag>.*)/$",
        LinkList.as_view(),
        name="link_list_tag"),
)
