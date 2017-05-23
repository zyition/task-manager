from django.db import models


class Member(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name


class Iteration(models.Model):
    name = models.CharField(max_length=64)
    date_created = models.DateTimeField(auto_now_add=True)
    planned_time = models.FloatField(default=0)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('tasks:list', args=[self.name])

    def __unicode__(self):
        return 'Iteration - %s' % self.name

    class Meta:
        ordering = ['-date_created']


class Task(models.Model):
    iteration = models.ForeignKey(Iteration)
    ticket_id = models.IntegerField(unique=True)
    summary = models.CharField(max_length=512)
    owner = models.ForeignKey(Member, null=True, blank=True)
    estimated_hours = models.FloatField(default=0)
    frozen = models.BooleanField(default=False)
    need_review = models.BooleanField(default=False)
    review_time = models.FloatField(default=0)
    ordering = models.IntegerField(default=0)

    def __unicode__(self):
        return '#%s' % self.ticket_id

    class Meta:
        ordering = ['ordering']
