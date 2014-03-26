from django import template
from django.template.defaultfilters import stringfilter
from .. import tools

register = template.Library()

@register.filter
def datestr(date):
    return tools.datestr(date)