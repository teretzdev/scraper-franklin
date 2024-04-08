 #!/bin/bash



 REPO_URL="https://github.com/teretzdev/scraper-franklin"

 LOCAL_DIR="./"

 COMMAND="npm install"



 while true; do

   git -C $LOCAL_DIR pull origin master



   diff=$(diff -r "$REPO_URL" "$LOCAL_DIR")

   if [ -n "$diff" ]; then

     echo "There are differences between the GitHub repo and local directory."

     echo "$diff"

     eval "$COMMAND"

   else

     echo "There are no differences between the GitHub repo and local directory."

   fi



   sleep 300 # wait 5 minutes

   COMMAND="RUN_ME.bat"

 done
