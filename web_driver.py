from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options

class web_driver():

    def __init__(self, browser, environment):
        self.browser = browser
        if self.browser=="firefox":
            self.driver = webdriver.Firefox()
        elif self.browser=="firefox_headless":
            options = Options()
            options.headless = True
            self.driver = webdriver.Firefox(options=options)
        elif self.browser=="chrome":
            self.driver = webdriver.Chrome()
        elif self.browser=="chrome_headless":
            chrome_options = Options()  
            chrome_options.add_argument("--headless") 
            self.driver = webdriver.Chrome(chrome_options=chrome_options)
        else:
            raise Exception("** Invalid browser **")
        self.environment = environment

    def getInstance(self):
        #Creation of Firefox Webdriver
        print('Environment: '+self.environment)
        print('Browser: '+self.browser)
        return self.driver
