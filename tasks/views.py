from collections import defaultdict
import json


from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST

from .forms import TaskConvertForm, AddTaskForm
from .models import Iteration, Task, Member
from .utils import update_task_ordering


def index(request):
    iterations = Iteration.objects.select_related().all()
    ctx = {
        'iterations': iterations,
    }
    return render(request, 'index.html', ctx)


def batch_import(request):
    ctx = {}
    if request.POST:
        form = TaskConvertForm(request.POST)
        if form.is_valid():
            task_list = form.cleaned_data['tasks']
            ctx['task_list'] = task_list
    else:
        form = TaskConvertForm()
    ctx['form'] = form
    return render(request, 'import.html', ctx)


def confirm_import(request):
    if request.POST:
        data = request.POST

        tasks_count = int(data.get('tasks_count'))
        iteration_name = data.get('iteration', "").strip()
        planned_time = data.get('planned_time')

        if not iteration_name:
            raise
        iteration, __ = Iteration.objects.get_or_create(name=iteration_name)
        iteration.planned_time = planned_time
        iteration.save()

        for i in range(tasks_count):
            number = data.get('task_number_%d' % i)
            if not number:
                continue
            summary = data.get('task_summary_%d' % i, "")
            number = number.strip().strip('#')
            summary = summary.strip()
            Task.objects.update_or_create(
                ticket_id=number, defaults={'summary': summary, 'iteration': iteration, 'ordering': i})

        messages.info(request, 'Import Successfully!')
        return redirect(iteration)


def add_task(request, iteration):
    iteration = get_object_or_404(Iteration, name=iteration)
    if request.method == 'GET':
        form = AddTaskForm(initial={"iteration": iteration})
    else:
        form = AddTaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Add Successfully!")
            return redirect(iteration)
    return render(request, 'add.html', {'form': form})


def list_task(request, iteration):
    iteration = get_object_or_404(Iteration, name=iteration)
    owner_mapping = dict(Member.objects.values_list('id', 'name'))
    owner_mapping.update({
        '': '-----',
        'selected': ''
    })
    ctx = {
        'iteration': iteration,
        'owner_select': json.dumps(owner_mapping),
    }
    return render(request, 'list.html', ctx)


def export_task(request, iteration):
    iteration = get_object_or_404(Iteration, name=iteration)

    line_formatter = "%(ticket_id)s\t%(summary)s\t%(estimated_hours)s"
    if request.GET.get('with_owner'):
        line_formatter += "\t%(owner__name)s"
    query_args = ('ticket_id', 'summary', 'estimated_hours', 'owner__name', 'need_review', 'review_time')
    task_info_list = iteration.task_set.filter(frozen=False).exclude(estimated_hours=0).values(*query_args)
    lines = []
    total_hours = 0
    for task_info in task_info_list:
        _need_review = task_info.pop('need_review', False)
        if _need_review:
            task_info['estimated_hours'] += task_info['review_time']
        total_hours += task_info['estimated_hours']
        lines.append(line_formatter % task_info)
    lines.append('Total Hours: %s' % total_hours)
    result = "\r\n".join(lines)
    response = HttpResponse(result, content_type="text/html")
    response['Content-Disposition'] = 'attachment; filename="%s.txt"' % iteration.name

    return response


def calc_total_hours(request, iteration):
    iteration = get_object_or_404(Iteration, name=iteration)
    total_hours = 0
    for task in iteration.task_set.filter(frozen=False):
        estimated_hours = task.estimated_hours
        total_hours += estimated_hours
        if task.need_review:
            total_hours += task.review_time
    return HttpResponse(total_hours)


def calc_owner_hours(request, iteration):
    iteration = get_object_or_404(Iteration, name=iteration)
    owner_hours = defaultdict(int)
    for task in iteration.task_set.filter(frozen=False):
        owner = task.owner.name if task.owner else 'left'
        estimated_hours = task.estimated_hours
        owner_hours[owner] += estimated_hours
        if task.need_review:
            owner_hours[owner] += task.review_time
    return JsonResponse(owner_hours)


def group_tasks_by_owner(request, iteration):
    iteration = get_object_or_404(Iteration, name=iteration)
    owner_tasks = defaultdict(list)
    all_tasks = iteration.task_set.filter(frozen=False).exclude(estimated_hours=0).values_list(
        'owner__name', 'ticket_id', 'need_review')
    for owner, ticket_id, need_review in all_tasks:
        owner_tasks[owner].append((ticket_id, need_review))
    return JsonResponse(owner_tasks)


@require_POST
def update(request):
    data = request.POST
    task = get_object_or_404(Task, id=data.get('task_id'))
    attr = data.get('name')
    value = data.get('value')
    setattr(task, attr, value)
    task.save()
    if attr == "owner_id":
        value = task.owner.name
    else:
        value = getattr(task, attr)
    return HttpResponse(value)


def update_ordering(request):
    data = request.GET
    task = get_object_or_404(Task, id=data.get('task_id'))
    ordering = data.get('ordering')
    ordering = int(ordering)
    update_task_ordering(task, ordering)
    return HttpResponse('OK')


def freeze(request):
    data = request.GET
    task = get_object_or_404(Task, id=data.get('task_id'))
    frozen = data.get('frozen') == 'true'
    task.frozen = frozen
    task.save()
    return HttpResponse('OK')


def need_review(request):
    data = request.GET
    task = get_object_or_404(Task, id=data.get('task_id'))
    _need_review = data.get('need_review') == 'true'
    task.need_review = _need_review
    task.save()
    return HttpResponse('OK')
