from selenium import webdriver
from lib import environment


class BaseTest(object):
    def set_driver(self):
        self.driver = webdriver.Chrome(executable_path=environment.CHROME_DRIVER_PATH)

    def setup(self):
        self.set_driver()

    def teardown(self):
        self.driver.close()
