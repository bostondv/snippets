# Chmod all files and directories
find . -type d -print0 | xargs -0 chmod 0755
find . -type f -print0 | xargs -0 chmod 0644

#MySQL Dump (gzip)
mysqldump --opt -u user -ppass db | gzip > path/to/file.sql.gz

#MySQL Import (gzip)
gunzip < path/to/file | mysql -u user -ppass db

#Find git config, change filemode to true recursively
find . -name config -print0 | xargs -0 sed -i "" "s|filemode = false|filemode = true|g"