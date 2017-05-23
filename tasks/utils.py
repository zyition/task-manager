from django.db.models import F
from .models import Task


def update_task_ordering(task, ordering):
    tasks = Task.objects.filter(iteration=task.iteration)
    old_ordering = task.ordering
    if ordering == old_ordering:
        return
    if ordering > old_ordering:
        tasks.filter(ordering__gt=old_ordering, ordering__lte=ordering).update(ordering=F('ordering')-1)
    elif ordering < old_ordering:
        tasks.filter(ordering__gte=ordering, ordering__lt=old_ordering).update(ordering=F('ordering')+1)
    task.ordering = ordering
    task.save()
