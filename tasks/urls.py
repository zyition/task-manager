from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<iteration>[a-zA-Z0-9]+)/add/$', views.add_task, name="add"),
    url(r'^(?P<iteration>[a-zA-Z0-9]+)/list/$', views.list_task, name="list"),
    url(r'^(?P<iteration>[a-zA-Z0-9]+)/export/$', views.export_task, name="export"),
    url(r'^(?P<iteration>[a-zA-Z0-9]+)/total-hours/$', views.calc_total_hours, name="total-hours"),
    url(r'^(?P<iteration>[a-zA-Z0-9]+)/owner-hours/$', views.calc_owner_hours, name="owner-hours"),
    url(r'^(?P<iteration>[a-zA-Z0-9]+)/tasks-by-owner/$', views.group_tasks_by_owner, name="tasks-by-owner"),
    url(r'^update/$', views.update, name="update"),
    url(r'^freeze/$', views.freeze, name="freeze"),
    url(r'^need-review/$', views.need_review, name="need-review"),
    url(r'^ordering-update/$', views.update_ordering, name="update-ordering"),
    url(r'^import/$', views.batch_import, name="import"),
    url(r'^import/confirm/$', views.confirm_import, name="import-confirm"),
]
