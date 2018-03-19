#!/usr/bin/env python
# encoding: utf-8

from django.test import TestCase
from rest_framework_jwt.settings import api_settings

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


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
        decoded_token = jwt_decode_handler(resp.json()['token'])
        self.assertTrue(decoded_token.get('id') == 1)
        self.assertTrue(decoded_token.get('username') == 'testuser1')

    def test_obtain_authtoken_wrong_password(self):
        resp = self.client.post(
            '/api/v1/accounts/obtain-auth-token/',
            {
                'username': 'testuser1',
                'password': 'wrongpassword'
            }
        )

        self.assertEqual(resp.status_code, 400)