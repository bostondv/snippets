from __future__ import with_statement
from fabric.api import *
import urllib

# Find and replace function
def replace_all(data, dic):
    for i, j in dic.iteritems():
        data = data.replace(i, j)
    return data

# Create wp-config.php
@task
def config():
	salt = urllib.urlopen('https://api.wordpress.org/secret-key/1.1/salt/').read()

	reps = {
		'database_name_here': env.dbname,
		'username_here': env.dbuser, 
		'password_here': env.dbpass,
		'localhost': env.dbhost,
		'//salt': salt,
	}

	config_sample = urllib.urlopen('https://raw.github.com/bostondv/snippets/master/wordpress/wp-config.php').read()
	config_file = open('wp-config-tmp.php','w')
	output = replace_all(config_sample, reps)
	config_file.write(output)
	config_file.close()
	with cd(env.dir):
		put('wp-config-tmp.php', 'wp-config.php')
		local('rm wp-config-tmp.php')

# Create .htaccess
@task
def htaccess():
	htaccess_sample = urllib.urlopen('https://raw.github.com/bostondv/snippets/master/wordpress/.htaccess').read()
	htaccess_file = open('htaccess-sample.txt','w')
	htaccess_file.write(htaccess_sample)
	with cd(env.dir):
		put('htaccess-sample.txt', '.htaccess')
		local('rm htaccess-sample.txt')