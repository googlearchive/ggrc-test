for x in `ps ux | grep "java.*selenium.*standalone" | awk '{print $2}'`
do
kill $x
done
killall Xvfb
killall chromedriver
