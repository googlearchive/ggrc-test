for x in `ps ux | grep "java.*selenium.*standalone" | grep -v "grep" | awk '{print $2}'`
do
kill $x
done
for x in `ps ux | grep "Xvfb" | grep -v "grep" | awk '{print $2}'`
do
kill $x
done
for x in `ps ux | grep "chromedriver" | grep -v "grep" | awk '{print $2}'`
do
kill $x
done
