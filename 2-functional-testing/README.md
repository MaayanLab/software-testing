# Functional testing
_Gregory Gundersen, Ma'ayan Lab meeting, 8 April 2015_

## Install Selenium

[Selenium](http://selenium-python.readthedocs.org/index.html) is open-source software for web browser automation. It is useful for testing because we can quickly and consistently mock a user of our web application. To install Selenium with `pip`, execute:
```
pip install selenium
```

## Basics of functional testing

> **What is the difference between functional and unit testing?**

- A **unit test** verifies that an individual unit of code works as expected, isolating it and mocking its dependencies.
- A **functional test** verifies that a slice of functionality in a system works as expected. This may test many methods (or units), interact with dependencies, modify a database, use web services, and so on.

> **What is a "functional slice"?**

There isn't a precise definition, but I prefer to think of it as unit of functionality at the level of user experience. For example, a functional test might verify that creating a new user works as expected or that menu options are different depending on if a user is logged in or not.

> **Why should I write functional test?**

For the [same reasons you write unit tests](https://github.com/MaayanLab/software-testing/blob/master/1-unit-testing/README.md): **stability**, **modularization**, **scalability**, etc.

> **When should I write functional tests?**

For scientists and researchers, unit tests are probably more important than functional tests because they allow us to directly verify that complex algorithms work—and continue to work—as expected. That said, functional tests can give you a measure of comfort in knowing that the basic aspects of your web application work across deployments.

Since many of our applications share a typical pipeline, `input gene list -> analysis -> output to user`, verifying that functional slice is probably a good start.

## Browser automation with Selenium

Since we primarily build web applications, we can write our functional tests by automating the browser with Selenium. Here's an example:

```python
from selenium import webdriver

# Create an instance of the Firefox web browser. There are drivers for other 
# browsers available, but this one ships with Selenium.
browser = webdriver.Firefox()

# Make a GET request to the URL passed in.
browser.get('http://www.google.com')

# Use Selenium's API to select and input text into the input field.
input_ = browser.find_element_by_id("lst-ib")
input_.send_keys('test')

# Select and click the submit button.
submit_btn = browser.find_element_by_id('sblsbb')
submit_btn.click()
```

## Wrapping Selenium with the `unittest` module

Last time, we discussed writing unit tests using Python's built-in `unittest` module. We can integrate our functional tests into the same framework, allowing us to execute unit and functional tests in the same suite. Here's [an example of testing Enrichr's interface](test_enrichr.py):

```python
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

        # Enrichr takes a second to Enrichr the results.
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
```