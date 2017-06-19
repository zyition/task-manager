from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import Iteration


# Test cases for models.

# Test cases for views
class IndexViewTests(TestCase):
    def test_no_iteration(self):
        response = self.client.get(reverse('tasks:index'))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "No Tasks!")

    def test_with_iterations(self):
        Iteration.objects.create(name="IR102")
        response = self.client.get(reverse('tasks:index'))
        self.assertEquals(response.status_code, 200)
        self.assertQuerysetEqual(response.context["iterations"], ["<Iteration: Iteration - IR102>"])