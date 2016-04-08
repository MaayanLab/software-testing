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
        with open('assets/genes.txt') as f:
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
        self.response = json.loads(response.text)

        # Enrichr returns an ID before saving the list. We need to wait for
        # it to catch up.
        time.sleep(2)

    def test_response_has_user_list_id(self):
        pass

    def test_response_has_short_id(self):
        pass

    # TODO: Implement this function.
    # Hint: Enrichr will return the list you just input if you make a GET
    #       request to:
    #       http://amp.pharm.mssm.edu/Enrichr/view?userListId={USER LIST ID}
    # Hint: Try using `assertListEqual()` to compare two lists. Remember
    #       that order is important.
    def test_input_against_output(self):
        pass

