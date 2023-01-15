from django.http import response
from django.test import TestCase, Client
from django.urls import reverse
from job.models import *
import json


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_login_url = reverse('admin_login')
        self.user_home_url = reverse('user_home')
        self.recruiter_home_url = reverse('recruiter_home')

    def test_user_home_view(self):
        response = self.client.get(self.admin_login_url)
        self.assertEqual(response.status_code, 200)

    def test_recruiter_home_view(self):
        response = self.client.get(self.recruiter_home_url)
        self.assertEqual(response.status_code, 302)

    def test_view_users(self):
        response = self.client.get(reverse('view_users'))
        self.assertEqual(response.status_code, 302)

    def test_delete_user(self):
        response = self.client.get(reverse('delete_user',args=['1']))
        self.assertEqual(response.status_code, 302)

    def test_change_status(self):
        response = self.client.get(reverse('change_status',args=['2']))
        self.assertEqual(response.status_code, 302)

    def test_view_all_recruiters(self):
        response = self.client.get(reverse('recruiter_all'))
        self.assertEqual(response.status_code, 302)

    def test_change_password_admin(self):
        response = self.client.get(reverse('change_passwordadmin'))
        self.assertEqual(response.status_code, 302)
