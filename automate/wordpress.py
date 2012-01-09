import os
import sys
import commands
import urllib

# 1. Create project dir
# 2. Create database
# 3. Download and unpack wordpress
# 4. Create wp-config.php
# 5. Create .htaccess
# 6. Download and install bones-repsonsive

usage = ("Automated WordPress Installer\n\n"
		"Usage: python wordpress.py app_name --prefix /path/to/install -u db_username -p db_password -d db_name -h db_host\n\n"
		"-u db_username  Database username\n"
		"-p db_password  Database password\n"
		"-d db_name      Database name\n"
		"-d db_host      Database host")

if len(sys.argv) < 2:
	print usage
	exit()

prefix = os.getcwd()
for key, value in enumerate(sys.argv):
		if value == '--prefix': 
			prefix = sys.argv[key + 1]

app = sys.argv[1]
prefix = prefix + '/' + app
gitosis_path = '/Users/bostondv/Files/workspace/gitosis-admin'

# Find and replace function
def replace_all(data, dic):
	for i, j in dic.iteritems():
		data = data.replace(i, j)
	return data

def wordpress(prefix):
	print '*** Downloading and unpacking WordPress source ***'
	os.system(	'mkdir -p ~/wptmp &&'
				'cd ~/wptmp &&'
				'curl -O http://wordpress.org/latest.tar.gz &&'
				'tar -xzf latest.tar.gz &&'
				'cp -r wordpress/ %s &&'
				'rm -r ~/wptmp'
				% (prefix))

def wp_config(app, prefix):
	print '*** Creating optimized and preconfigured wp-config ***'
	db_username = 'root'
	db_password = 'pom889DV'
	db_name = app
	db_host = 'localhost'

	for key, value in enumerate(sys.argv):
		if value == '-u': 
			db_username = sys.argv[key + 1]
		if value == '-p': 
			db_password = sys.argv[key + 1]
		if value == '-d': 
			db_name = sys.argv[key + 1]
		if value == '-h': 
			db_host = sys.argv[key + 1]
	
	salt = urllib.urlopen('https://api.wordpress.org/secret-key/1.1/salt/').read()

	reps = {
		'database_name_here': db_name,
		'username_here': db_username, 
		'password_here': db_password,
		'localhost': db_host,
		'//salt': salt,
	}

	config_path = '%s/wp-config.php' % (prefix)
	if os.path.exists(config_path):
		print config_path, 'already exists, skipping.'
		return
	else:
		config_sample = urllib.urlopen('https://raw.github.com/bostondv/snippets/master/wordpress/wp-config.php').read()
		config_file = open(config_path,'w')
		output = replace_all(config_sample, reps)
		config_file.write(output)
		config_file.close()

def wp_htaccess(prefix):
	print '*** Creating optimized .htaccess ***'
	htaccess_path = '%s/.htaccess' % (prefix)
	if os.path.exists(htaccess_path):
		print htaccess_path, 'already exists, skipping.'
		return
	else:
		htaccess_sample = urllib.urlopen('https://raw.github.com/bostondv/snippets/master/wordpress/.htaccess').read()
		htaccess_file = open(htaccess_path,'w')
		htaccess_file.write(htaccess_sample)

def wp_gitignore(prefix):
	print '*** Creating optimized .gitignore ***'
	ignore_path = '%s/.gitignore' % (prefix)
	if os.path.exists(ignore_path):
		print ignore_path, 'already exists, skipping.'
		return
	else:
		ignore_sample = urllib.urlopen('https://raw.github.com/bostondv/snippets/master/wordpress/gitignore.txt').read()
		ignore_file = open(ignore_path,'w')
		ignore_file.write(ignore_sample)

def wp_bones(app, prefix):
	print '*** Installing bones-responsive theme ***'
	theme_path = '%s/wp-content/themes/%s' % (prefix, app)
	if os.path.exists(theme_path):
		print theme_path, 'already exists, skipping.'
	else:
		os.system(	'cd %s &&'
					'git submodule add git://github.com/eddiemachado/bones-responsive.git wp-content/themes/%s &&'
					'git commit -am "adding bones responsive theme"' % (prefix, app))

def wp_thematic(app, prefix):
	print '*** Installing thematic ***'
	theme_path = '%s/wp-content/themes/thematic' % (prefix)
	if os.path.exists(theme_path):
		print theme_path, 'already exists, skipping.'
	else:
		os.system(	'cd %s &&'
					'git submodule add https://github.com/iridia/thematic.git wp-content/themes/thematic &&'
					'git commit -am "adding thematic theme"' % (prefix))

def wp_thematic_child(app, prefix):
	print '*** Installing thematic child ***'
	theme_path = '%s/wp-content/themes/%s' % (prefix, app)
	if os.path.exists(theme_path):
		print theme_path, 'already exists, skipping.'
	else:
		os.system(	'wget "https://github.com/bostondv/thematic-child/tarball/master" -O ~/tmp/thematic-child.tar.gz &&'
					'tar -C %s/wp-content/themes/ -xzf ~/tmp/thematic-child.tar.gz &&'
					'mv %s/wp-content/themes/bostondv-thematic-child-* %s &&'
					'cd %s &&'
					'git add . &&'
					'git commit -am "adding thematic child theme"' % (prefix, prefix, theme_path, prefix))

def wp_hybrid(app, prefix):
	print '*** Installing hybrid ***'
	theme_path = '%s/wp-content/themes/hybrid' % (prefix)
	if os.path.exists(theme_path):
		print theme_path, 'already exists, skipping.'
	else:
		os.system(	'wget "http://wordpress.org/extend/themes/download/hybrid.1.0.zip" -O ~/tmp/hybrid.zip &&'
					'tar -C %s/wp-content/themes/ -xzf ~/tmp/hybrid.zip &&'
					'cd %s &&'
					'git add . &&'
					'git commit -am "adding hybrid theme"' % (prefix, prefix))

def wp_hybrid_skeleton(app, prefix):
	print '*** Installing hyrbid child skeleton ***'
	theme_path = '%s/wp-content/themes/%s' % (prefix, app)
	if os.path.exists(theme_path):
		print theme_path, 'already exists, skipping.'
	else:
		os.system(	'wget "https://github.com/bostondv/hybrid-child/tarball/master" -O ~/tmp/hybrid-child.tar.gz &&'
					'tar -C %s/wp-content/themes/ -xzf ~/tmp/hybrid-child.tar.gz &&'
					'mv %s/wp-content/themes/bostondv-hybrid-child-* %s &&'
					'cd %s &&'
					'git add . &&'
					'git commit -am "adding hybrid child skeleton theme"' % (prefix, prefix, theme_path, prefix))

def gitosis(app, prefix, gitosis_path):
	print '*** Creating Gitosis entries ***'
	output = (	'\n\n[group %s]\n'
				'members = pomelo bostondv\n'
				'writable = %s' % (app, app))
	gitosis_config = open('%s/gitosis.conf' % (gitosis_path),'r+a')
	text = gitosis_config.read()
	search = '[group %s]' % (app)
	index = text.find(search)
	if index > -1:
		print search, 'already found in config file at', index, '. skipping gitosis.'
		return
	else:
		gitosis_config.write(output)
		gitosis_config.close()
		os.system(	'cd %s &&'
					'git commit -am "Adding %s repository" &&'
					'git push' % (gitosis_path, app))

def git_init(app, prefix):
	print '*** Creating Git repository and pushing first commit ***'
	os.system(	'cd %s &&'
				'git init &&'
				'git add . &&'
				'git commit -am "Initial project setup" &&'
				'git remote add origin git@pomelodesign.com:%s.git' % (prefix, app))

def git_push(prefix):
	print '*** Git push ***'
	os.system('cd %s && git push -u origin master' % (prefix))

def db(app):
	print '*** Creating MySQL database ***'
	sql = 'CREATE DATABASE %s;' % (app)
	os.system('mysql -u root -p -e "%s"' % (sql))

def hosts(app):
	print '*** Adding entry to /etc/hosts ***'
	output = (	'\n127.0.0.1     %s.local\n'
				'fe80::1%%lo0     %s.local' % (app, app))
	hosts_path = '/etc/hosts'
	hosts_file = open(hosts_path,'r+a')
	text = hosts_file.read()
	search = '%s.local' % (app)
	index = text.find(search)
	if index > -1:
		print search, 'already found in hosts file at', index, '. skipping hosts.'
		return
	else:
		hosts_file.write(output)
		hosts_file.close()

def fabfile(prefix):
	print '*** Installing fabfile ***'
	os.system(	'cd %s &&'
				'git submodule add git://github.com/bostondv/fabfile.git &&'
				'git commit -am "adding fabfile"' % (prefix))
	return

def install(app, prefix, gitosis_path):
	print '*** Installing new wordpres-s app:', app, 'at', prefix, '***'
	if os.path.exists(prefix):
		print '%s already exists. Please re-run with a new path' % (prefix)
		exit()
	os.system('mkdir -p %s' % (prefix))
	wordpress(prefix)
	wp_config(app, prefix)
	wp_htaccess(prefix)
	wp_gitignore(prefix)
	db(app)
	#hosts(app)
	gitosis(app, prefix, gitosis_path)
	git_init(app, prefix)
	fabfile(prefix)
	wp_hybrid(app, prefix)
	wp_hybrid_skeleton(app, prefix)
	git_push(prefix)
	print '*** And we\'re done.', app, 'installed to', prefix + '.\n'
	print '*** Go to http://' + app + '.local/ to complete installation.\n' 
	print 'Don\'t forget to add', app, 'to your hosts file!'

# Execute the functions
install(app, prefix, gitosis_path)
