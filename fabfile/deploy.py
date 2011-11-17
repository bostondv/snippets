from __future__ import with_statement
from fabric.api import *

# Deploy the website
@task(default=True)
def run():
	with settings(warn_only=True):
		if run('test -d %s/.git' % (env.dir)).failed:
			if run('test -f %s/index.html' % (env.dir)).succeeded:
				run('rm %s/index.html' % (env.dir))
			execute(deploy.setup)
		else:
			execute(git.commit)
			execute(git.push)
			execute(git.pull_remote)

# Create tmp dirs
@task
def scaffolding():
	with cd(env.dir):
		run('mkdir -p %s' % (env.media))
		run('mkdir -p %s' % (env.dbpath))
	run('mkdir -p ~/tmp')
	local('mkdir -p ~/tmp')
	local('mkdir -p %s' % (env.media))
	run('db -p %s' % (env.dbpath))

# First run install - automatically triggered by 'deploy' if needed
@task
def setup():
	execute(deploy.scaffolding)
	execute(git.commit)
	execute(git.push)
	run('git clone %s:%s.git %s' % (env.git, env.app, env.dir))
	execute(wordpress.config)
	execute(wordpress.htaccess)
	execute(media.put)
	execute(deploy.db)

# Deploy the database
@task
def db():
	execute(db.dump_remote)
	execute(db.dump)
	execute(db.put)
	execute(db.mysql_remote)

# Update local development from remote
@task
def get():
	execute(db.dump)
	execute(db.dump_remote)
	execute(git.commit_remote)
	execute(git.push_remote)
	execute(git.pull)
	execute(media.get)
	execute(db.mysql)