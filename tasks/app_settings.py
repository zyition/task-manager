from django.conf import settings

task_link_pattern = getattr(settings, 'TASK_LINK_PATTERN', None)
