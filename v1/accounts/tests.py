#!/usr/bin/env python
# encoding: utf-8

from django.test import TestCase


class AccountTests(TestCase):
    fixtures=['test/users.json']

    def test_obtain_authtoken_success(self):
        resp = self.client.post(
            '/api/v1/accounts/obtain-auth-token/',
            {
                'username': 'testuser1',
                'password': 'testpassword'
            }
        )

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json()['id'] == 1)
        self.assertTrue(len(resp.json()['token']) == 40)

    def test_obtain_authtoken_wrong_password(self):
        resp = self.client.post(
            '/api/v1/accounts/obtain-auth-token/',
            {
                'username': 'testuser1',
                'password': 'wrongpassword'
            }
        )

        self.assertEqual(resp.status_code, 400)