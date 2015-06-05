from django.db import models
from django.utils.safestring import mark_safe


class SQLReport(models.Model):
    """It will contains sqlreports sql query
    """
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    query = models.TextField()
    user_allowed = models.BooleanField(default=False,
        help_text="Set to true to allow any user to execute a sqlreports. Risky!")

    def __unicode__(self):
        return self.name

    def go_to_report(self):
        return mark_safe('<a href="/sql-reports/{0}/"/>Go To SQLReport</a>'.format(self.id))


class SQLReportParam(models.Model):
    """It will contains sqlreports sql query with params
    """
    report = models.ForeignKey(SQLReport)
    param_key = models.CharField(max_length=128)
    display_name = models.CharField(max_length=128, default='', blank=True)
    help_text = models.CharField(max_length=512, default='', blank=True)
    choices = models.CharField(max_length=2045, help_text='Comma separated choices', default='', blank=True)

    @property
    def choice_list(self):
        return [x.strip() for x in self.choices.split(',')]
