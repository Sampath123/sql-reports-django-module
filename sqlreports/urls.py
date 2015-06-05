from django.conf.urls import patterns, url
from sqlreports.views import sql_reports, sql_report

urlpatterns = patterns('',
    url(r'^$', sql_reports, name='report_list'),
    url(r'^(?P<report_id>\d+)/$', sql_report, name='get_report')
)
