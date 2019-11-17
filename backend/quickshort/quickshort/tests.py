from django.test import TestCase

# Create your tests here.
import logging
import unittest
from django.test import Client
import json

logging.basicConfig(level=logging.DEBUG)

class SimpleTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        response = self.client.post('/create/', data={"url":"https://www.google.com"}, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        resp = response.json()
        stats_key = resp['stats_key']
        short_url = resp['short_url']
        logging.info(f"key={stats_key} short_url={short_url}")
        response = self.client.get("/" + short_url + "/")
        self.assertEqual(response.status_code, 302)
        # logging.info(response.body)

        response = self.client.post('/create/', data={"url":"https://www.google3.com"}, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        resp = response.json()
        stats_key = resp['stats_key']
        short_url = resp['short_url']
        logging.info(f"key={stats_key} short_url={short_url}")
        response = self.client.get("/" + short_url + "/")
        self.assertEqual(response.status_code, 302)

        # Check that the rendered context contains 5 customers.
        # self.assertEqual(len(response.context['customers']), 5)