To be able to run UI automation test scripts on your local machine, you need to have your machine setup correctly with all needed software and libraries installed.  
These instructions below is applicable to MAC OS, LINUX, or UNIX.	Execute in a terminal	Your computer might have different installer and I suppose you know how to install:  easy_install or apt-get or rpm.
		
To Get Automation Test from GitHub, do:	
git clone http://github.com/reciprocity/ggrc-test	
It will creates a folder ggrc-test in your home directory with all the automation data.  Make sure you have permission to clone.
		
To set up your computer for automation, do these:		
- install python by doing: easy_install python for MAC, or  apt-get install python (Linux).
  You need to prefix "sudo" to the command.  For example, sudo apt-get install python.  Type "python --version", and it should prints Python 2.7.5 

- install Selenium WebDriver by doing: easy_install selenium or pip install selenium	
- download chromedriver from https://sites.google.com/a/chromium.org/chromedriver/downloads  and put it in /usr/bin/ (MAC) directory		
- set up PYTHONPATH	export PYTHONPATH=/Users/your_user_name/ggrc-test .	 If you don't set up the path, you will have to do "export PYTHONPATH=." in ggrc-test every time before you are able to run a script.
		
- install nosetests which is the unittest frame work for Python, akin to Junit for Java	by doing: easy_install nose or pip install nose	
		
Need to update the config.py file before running:	must be in ggrc-test directory	This configuration file allows you the flexibility to change data in one place.
- edit parameter url to point to your test site		
- edit parameter use_remote_webdriver to False if you use webdriver from your machine which is like to be the case by setting: use_remote_webdriver = bool(False) .	
  If you skip this step, you WILL NOT see test executing on your display but instead at reciprocitylabs.com. 
- enter the username and password that you want to log in with by setting:	"username = os.getenv('TEST_SITE_USERNAME', "your_username"), 
  password = os.getenv('TEST_SITE_PASSWORD', "your_password")" .
		
Run a script:		
-from ggrc-test directory, you can execute a test either with python or nose .   For example,	python Create/TestContractCreate.py or nosetests Create/TestContractCreate.py	
			
Tip for elements:		
- if ID exists use it (best stuff on earth)		
- Xpath is easier to write but very susceptible to changes if element is move around		
- CSS selector is like Xpath but it has an advantage; no html tag is needed.  As long as the attribute is the same it can be moved around without affect.  Sometime is it harder to write compare to xpath.		
- use custom attribute "data-id" for element and add that to mustache file and submit merge request.   Make sure cares need to be taken serriously because GGRC is using this mustache file to format data, and you don't want to screw it up.		