import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from sqlreports import api, utils
from sqlreports.models import SQLReportParam, SQLReport
from django.core.exceptions import PermissionDenied


@login_required
def sql_reports(request):
    """Lists all the available sqlreports for the current user.
       TODO: Filter on available sqlreports.
    """
    filters = {}
    if not request.user.is_superuser:
        filters['user_allowed'] = True

    return render_to_response('sqlreports/sqlreports.html',
                              {
                               "sqlreports": SQLReport.objects.\
                                          filter(**filters).order_by('name')
                               },
                              RequestContext(request))


@login_required
def sql_report(request, report_id):
    """
    For given sqlreports id and params
    it will generate the sqlreports tables
    """
    report = SQLReport.objects.get(pk=report_id)
    _validate_report_access(request.user, report)
    is_csv = request.GET.get("is_csv", False)
    is_html = request.GET.get("is_html", False)
    param_dict, params = _get_param_dict(request, report_id)

    context_to_send = {
                       'report': report,
                       'params': params,
                       'is_html': is_html,
                       'param_dict': param_dict
                       }
    if is_csv or is_html:
        try:
            report_data = api.get_report_data(report_id, param_dict)
            headers = report_data[0].keys()
            context_to_send.update({
                                    'report_data': report_data,
                                    'headers': headers})
        except IndexError:
            error_msg = "No data available for this sqlreports"
            context_to_send.update({'error_msg': error_msg})

        if is_csv:
            report_file_name = report.name
            report_file_name = "%s_%s.csv" % (report_file_name,
                                              str(datetime.datetime.now()))
            report_file_name = report_file_name.replace(" ", "-")
            return utils.download_csv_python_obj(headers, report_data,
                                                 file_name=report_file_name)

    return render_to_response('sqlreports/sqlreport.html', context_to_send,
                               RequestContext(request))


def _get_param_dict(request, report_id):
    param_dict = {}
    params = SQLReportParam.objects.filter(report_id=report_id)
    for param in params:
        param_key = request.GET.get(param.param_key)
        if param_key:
            param_dict.update({param.param_key: param_key})
    return (param_dict, params)


def _validate_report_access(user, report):
    '''Validates if running a sqlreports is allowed or not'''
    # TODO: Instead of this provide hook.

    if user.is_superuser:
        # Super users are allowed everything
        return True

    if not user.is_staff:
        # Non Staff are never allowed access to sqlreports
        raise PermissionDenied("SQLReport access is not allowed.")

    # Allowed only if sqlreports is designated as a non-super user allowed
    if not report.user_allowed:
        raise PermissionDenied("SQLReport access is not allowed.")

    return True
