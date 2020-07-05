cd temp/vol
set arg1=%1
set arg2=%2
git init
git add .
git remote add origin https://github.com/%arg1%/%arg2%.git
git commit -m "Test files"
git push -u origin master
pause