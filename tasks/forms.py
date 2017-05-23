import re
from StringIO import StringIO

from django import forms
from django.db.models import F
from django.forms.utils import ErrorList

from .models import Task

task_info_cpt = re.compile(r'(^#\d+)(.*$)', re.I)


class TaskConvertForm(forms.Form):
    iteration = forms.CharField()
    planned_time = forms.FloatField(required=False)
    tasks = forms.CharField(label=u'Tasks Information', widget=forms.Textarea)

    def clean_tasks(self):
        tasks = self.cleaned_data.get('tasks')
        task_list = []
        if tasks:
            for line in StringIO(tasks):
                line = line.strip()
                task_info = task_info_cpt.findall(line)
                if task_info:
                    task_list.extend(task_info)
        if task_list:
            return task_list
        else:
            raise forms.ValidationError('Invalid Tasks Information.')


class AddTaskForm(forms.ModelForm):
    def __init__(
            self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
            label_suffix=None, empty_permitted=False, instance=None):
        if data is not None:
            ticket_id = data.get('ticket_id')
            if ticket_id:
                task = Task.objects.filter(ticket_id=ticket_id).first()
                if task is not None:
                    instance = task
        super(AddTaskForm, self).__init__(
            data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, instance)

    class Meta:
        model = Task
        exclude = ()
        widgets = {
            'iteration': forms.HiddenInput,
        }

    def save(self, commit=True):
        task = super(AddTaskForm, self).save(commit=commit)
        ordering = task.ordering
        base_query = Task.objects.filter(iteration=task.iteration)
        if task.id is not None:
            base_query = base_query.exclude(id=task.id)
        if base_query.filter(ordering=ordering).exists():
            base_query.filter(ordering__gte=ordering).update(ordering=F('ordering')+1)
        return task
