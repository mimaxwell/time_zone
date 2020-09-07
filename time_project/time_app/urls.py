from django.urls import path, re_path
from .views import UnixTime, UTCTime, ZoneTime, ZoneTimeDetail, ZoneTimeName, ZoneTimeOffset, ZoneTimeNameOffset

urlpatterns = [
    path('unix/', UnixTime.as_view()),
    path('utc/', UTCTime.as_view()),
    path('zone/',  ZoneTime.as_view()),
    path('zone/<int:pk>/', ZoneTimeDetail.as_view()),
    re_path(r'^zone/(?P<name>[A-Z]{3})/offset', ZoneTimeNameOffset.as_view()),
    re_path(r'^zone/(?P<name>[A-Z]{3})/', ZoneTimeName.as_view()),
    re_path(r'^zone/(?P<offset>(\+|\-)(10|11|[0-9]))', ZoneTimeOffset.as_view()),
]


