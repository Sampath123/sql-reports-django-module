import MySQLdb
from collections import OrderedDict

from django.db import connection
from django.template import Context, Template
from sqlreports.models import SQLReport


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        OrderedDict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def get_report_query(report_id, params):
    """ QueryExample:
    select id, checkin_time from auth_user where email = '{{EMAIL_ID}}'
    """
    # FIXME: Need to include MySQL Escape
    query = SQLReport.objects.get(id=report_id).query
    t = Template(query)

    # Escaping Params
    escaped_params = {}
    for item in params.items():
        escaped_params[item[0]] = MySQLdb.escape_string(item[1])
    c = Context(escaped_params)
    return t.render(c)


def get_report_data(report_id, params):
    """ For given sqlreports id and params it return the sqlreports data"""
    # FIXME: Connection should have only read only permission
    query = get_report_query(report_id, params)
    cursor = connection.cursor()
    cursor.execute(query)
    return dictfetchall(cursor)

