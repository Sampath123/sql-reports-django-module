from django.contrib import admin
from sqlreports.models import SQLReportParam, SQLReport


class SqlReportParamInlineAdmin(admin.TabularInline):
    model = SQLReportParam
    extra = 1


class SqlReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'go_to_report')
    inlines = [
        SqlReportParamInlineAdmin
    ]

admin.site.register(SQLReport, SqlReportAdmin)
