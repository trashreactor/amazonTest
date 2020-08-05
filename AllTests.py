import unittest
from pyunitreport import HTMLTestRunner
from selenium import webdriver
from Locators import Locators
from TestData import TestData
import Pages
from Pages import HomePage, SearchResultsPage, ProductDetailsPage, SubCartPage, CartPage, SignInPage

# Base Class for the tests
class Test_Amazon_Search_Base(unittest.TestCase):

    def setUp(self):
        # Setting up how firefox will run
        # firefox_options=webdriver.FirefoxOptions()
        # firefox_options.add_argument('headless')
        # firefox_options.add_argument('window-size=1920x1080')
        # print ("Browser Path:   " + TestData.BROWSER_EXECUTABLE_PATH + "  ends here")
        # self.driver=webdriver.Chrome(TestData.BROWSER_EXECUTABLE_PATH, options=chrome_options)
        self.driver=webdriver.Firefox()
        #browser should be loaded in maximized window
        self.driver.maximize_window()
    
    def tearDown(self):
        self.driver.close()
        self.driver.quit()

# Test Class containing all tests
class Test_Amazon_Search(Test_Amazon_Search_Base):
    def setUp(self):
        super().setUp()

    def test_1_home_page_should_load(self):
        # instantiate an object of HomePage class. 
        # it opens up the browser and navigates to Home Page of the site under test.
        self.homePage=HomePage(self.driver)
        # assert if the title of Home Page contains Amazon.in
        self.assertIn(TestData.HOME_PAGE_TITLE, self.homePage.driver.title)

    def test_2_user_should_be_able_to_search(self):
        self.homePage=HomePage(self.driver)
        # search for the search term on Home Page. 
        # The search term would be picked from TestData.py file
        self.homePage.search()
        # instantiate an object of SearchResultsPage class passing in the driver as parameter.
        # this will allow the newly created object to have access to the browser and perform
        # webdriver operations.
        self.searchResultsPage=SearchResultsPage(self.homePage.driver)
        # assert that the search term indeed return some results.
        self.assertNotIn(TestData.NO_RESULTS_TEXT,self.searchResultsPage.driver.page_source)
    
    def test_3_user_should_be_able_to_add_item_to_cart(self):
        self.homePage=HomePage(self.driver)
        self.homePage.search()
        self.searchResultsPage=SearchResultsPage(self.homePage.driver)
        # click on the first search result
        self.searchResultsPage.click_search_result()
        # instantiate an object of Product Details Page class
        self.productDetailsPage=ProductDetailsPage(self.searchResultsPage.driver)
        # click on the Add To Cart button
        self.productDetailsPage.click_add_to_cart_button()
        # instantiate an object of Sub Cart Page class
        self.subCartPage=SubCartPage(self.productDetailsPage.driver)
        # assert if the sub cart page has indeed loaded
        self.assertTrue(self.subCartPage.is_enabled(Locators.SUB_CART_DIV))
        # assert if the product was added to the cart successfully
        self.assertTrue(self.searchResultsPage.is_visible(Locators.PROCEED_TO_BUY_BUTTON))

    def test_4_user_should_be_able_to_delete_item_from_cart(self):
        self.homePage=HomePage(self.driver)
        self.homePage.search()
        self.searchResultsPage=SearchResultsPage(self.homePage.driver)
        self.searchResultsPage.click_search_result()
        self.productDetailsPage=ProductDetailsPage(self.searchResultsPage.driver)
        self.productDetailsPage.click_add_to_cart_button()
        self.subCartPage=SubCartPage(self.productDetailsPage.driver)
        # click on the Cart's hyperlink to load the cart page
        self.subCartPage.click_cart_link()
         # instantiate an object of Cart Page class
        self.cartPage=CartPage(self.subCartPage.driver)
        # find the cart count before deleting an item from the cart
        cartCountBeforeDeletion=int(self.driver.find_element(*Locators.CART_COUNT).text)
        # delete an item from cart
        self.cartPage.delete_item()
         #to assert the item was deleted successfully
        self.assertTrue(int(self.driver.find_element(*Locators.CART_COUNT).text) < cartCountBeforeDeletion) 

if __name__ == '__main__':
    unittest.main(testRunner=HTMLTestRunner(output=''))