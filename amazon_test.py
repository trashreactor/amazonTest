from pyunitreport import HTMLTestRunner
import unittest
import web_driver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class AmazonTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        wd = web_driver.web_driver('firefox','https://www.amazon.com/')
        self.driver = wd.getInstance()
        self.environment = wd.environment
        # set implicit wait time 
        self.driver.implicitly_wait(10) # seconds 

    def test_1_searchItem_AddItemToCart(self):
        driver = self.driver
        # get url 
        driver.get(self.environment)
        # Assert page title
        self.assertIn("Amazon.com", driver.title)
        # Enter text in textbard and click on search
        elem = driver.find_element_by_id("twotabsearchtextbox")
        elem.send_keys("backpack hustle 4.0")
        elem.send_keys(Keys.RETURN)
        # find and click on login link
        elem = driver.find_element_by_partial_link_text("Under Armour")
        elem.click()
        # Assert page title
        self.assertIn("Under Armour", driver.title)
        # Add item to cart
        elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'add-to-cart-button')))
        elem.click()
        # Assert that the success message is displayed
        elem = driver.find_element_by_id("huc-v2-order-row-confirm-text")
        self.assertEqual("Added to Cart",elem.text)
    
    def test_2_removeItemFromCart(self):
        driver = self.driver
        # Enter text in textbard and click on search
        elem = driver.find_element_by_id("nav-cart")
        elem.click()
        # Assert page title
        self.assertIn("Shopping Cart", driver.title)
        # Find and delete the item
        elem = driver.find_element_by_css_selector('[name^="submit.delete"]')
        elem.click()
        # Asser that the delete message is displayed
        elem = driver.find_element_by_class_name('sc-your-amazon-cart-is-empty')
        self.assertEqual('Your Amazon Cart is empty',elem.text)

    @classmethod
    def tearDownClass(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main(unittest.main(testRunner=HTMLTestRunner(output='amazonTest',report_title='AmazonTest')))