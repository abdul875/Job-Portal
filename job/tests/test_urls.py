from django.test import SimpleTestCase
from django.urls import reverse, resolve
from job.views import *


class TestUrls(SimpleTestCase):

    def test_admin_login_url_is_resolved(self):
        url = reverse('admin_login')
        self.assertEquals(resolve(url).func, admin_login)

    def test_user_login_url_is_resolved(self):
        url = reverse('user_login')
        self.assertEquals(resolve(url).func, user_login)
