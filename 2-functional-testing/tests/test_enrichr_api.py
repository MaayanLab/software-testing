"""Unit tests for Enrichr's API.
"""

import json
import requests
from requests.exceptions import ConnectionError
import time
import unittest


class TestEnrichr(unittest.TestCase):

    BASE_URL = 'http://amp.pharm.mssm.edu/Enrichr'

    def setUp(self):
        with open('tests/data/genes.txt') as f:
            self.input_genes = [l.strip().upper() for l in f]

        url = self.BASE_URL + '/addList'
        genes = '\n'.join(self.input_genes)
        payload = {
            'list': genes,
            'description': ''
        }
        response = requests.post(url, files=payload)
        if response.status_code != 200:
            raise ConnectionError('Unable to POST gene list.')
        self.resp = json.loads(response.text)

        # Enrichr returns an ID before saving the list. We need to wait for
        # it to catch up.
        time.sleep(2)

    def test_response_has_user_list_id(self):
        self.assertIn('userListId', self.resp)

    def test_response_has_short_id(self):
        self.assertIn('shortId', self.resp)

    def test_input_against_output(self):
        user_list_id = self.resp['userListId']
        resp = requests.get(self.BASE_URL + '/view?userListId=%s' % user_list_id)
        genes = json.loads(resp.text).get('genes')

        # Verify both gene lists are the same, after sorting.
        self.assertListEqual(sorted(genes), sorted(self.input_genes))

