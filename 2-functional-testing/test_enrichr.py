import unittest
import time

from selenium import webdriver


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

        # Enrichr takes a second to Enrichr the results.
        time.sleep(5)

        # Select enrichment terms and verify the first one
        terms = self.browser.find_elements_by_css_selector('svg > g')
        self.assertEqual(terms[0].text, 'E2F1_18555785_ChIP-Seq_MESC_Mouse')

    def tearDown(self):
        self.browser.quit()