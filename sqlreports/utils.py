import csv
from django.http import HttpResponse


def download_csv_python_obj(headers, data_objs, file_name="sqlreports.csv"):
    """For given python objects it will return the csv file"""
    response = HttpResponse(mimetype='text/csv')
    # force download.
    response['Content-Disposition'] = 'attachment;filename=%s' % file_name
    # the csv writer
    writer = csv.writer(response)
    field_names = [header for header in headers]
    # Write a first row with header information
    writer.writerow(field_names)
    # Write data rows
    for data_obj in data_objs:
        writer.writerow([data_obj[field] for field in field_names])
    return response

download_csv_python_obj.short_description = "Download selected as csv"
