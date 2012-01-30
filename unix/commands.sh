# Chmod all files and directories
find . -type d -print0 | xargs -0 chmod 0755
find . -type f -print0 | xargs -0 chmod 0644

find . -type d -print0 | xargs -0 sudo chmod 0755
find . -type f -print0 | xargs -0 sudo chmod 0644

#MySQL Dump (gzip)
mysqldump --opt -u user -ppass db | gzip > path/to/file.sql.gz

#MySQL Import (gzip)
gunzip < path/to/file | mysql -u user -ppass db

#Find git config, change filemode to true recursively
find . -name config -print0 | xargs -0 sed -i "" "s|filemode = false|filemode = true|g"

# Fix base64_decode hack
find . \( -name "*.php" \) -exec grep -Hn "[[:blank:]+]eval(base64_decode(.*));" {} \; -exec sed -i 's/[[:blank:]+]eval(base64_decode(.*));//g' {} \;

#Instant server for the current directory
alias server='open http://localhost:8000 && python -m SimpleHTTPServer'	

# Webfaction memory usage
ps -u pomelo -o rss,etime,pid,command