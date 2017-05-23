from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from tasks.app_settings import task_link_pattern


register = template.Library()


@register.filter()
def bind_link(ticket_id):
    if task_link_pattern:
        ticket_id = conditional_escape(ticket_id)
        link = task_link_pattern % ticket_id
        html_pattern = '<a href="%s" target="_blank">#%%s</a>' % link
    else:
        html_pattern = "#%s"

    return mark_safe(html_pattern % ticket_id)
