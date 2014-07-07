


import time
import unittest
from selenium import webdriver

class ukyoTest(unittest.TestCase):


    def test1(self):
        driver = webdriver.Chrome("/usr/local/bin/chromedriver")
        driver.get("http://localhost:8080")  #("http://yahoo.com")
        time.sleep(9)
        driver.quit()

        
if __name__ == "__main__":
        unittest.main()

