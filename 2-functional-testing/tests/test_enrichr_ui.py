"""Tests for Enrichr's user interface.
"""

import unittest
import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


class TestEnrichr(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.get('http://amp.pharm.mssm.edu/Enrichr/')

    def test_crisp_set_enrichment(self):
        # Submit the example crisp set.
        self.browser.find_element_by_id('insertCrispExample-link').click()
        self.browser.find_element_by_id('proceed-button').click()

        # Select the ChEA_2015 library results
        self.browser.find_element_by_id('ChEA_2015-link').click()

        # Wait while Enrichr performs analysis
        time.sleep(6)

        # Select enrichment terms and verify the first one
        terms = self.browser.find_elements_by_css_selector('svg > g')
        self.assertEqual(terms[0].text, 'E2F1_18555785_ChIP-Seq_MESC_Mouse')

        # Hover over enrichment term bar to see scores. Verify that all scores
        # are correct
        ActionChains(self.browser).move_to_element(terms[0]).perform()
        tooltip = self.browser.find_element_by_css_selector('#aToolTip')
        scores = tooltip.text.split('\n')
        self.assertEqual(scores[0], 'p-value: 9.661e-54')
        self.assertEqual(scores[1], 'q-value: 3.652e-51')
        self.assertEqual(scores[2], 'z-score: -1.22')
        self.assertEqual(scores[3], 'combined score: 141.20')

    def tearDown(self):
        self.browser.quit()
