# Script to set as build shell in Jenkins
sh killscript.sh
sleep 2
sh /home/jenkins/server/run-selenium.sh
sh /home/jenkins/server/run-selenium.sh  # randomly doesn't run the first time
sleep 10  # give it time to start completely or it doesn't work
nosetests SuiteAllTests.py --nocapture --with-xunit --xunit-file=SuiteAllTestsResults.xml
python helperRecip/Reporter.py  # write out time results
nosetests -v --nocapture Cleanup/ApiDeleteObjects.py
nosetests -v --nocapture Cleanup/Reindex.py
