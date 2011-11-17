from __future__ import with_statement
from fabric.api import *

# Put media local --> remote
@task
def put():
	local('tar czf ~/tmp/media.tgz %s' % (env.media))
	put('~/tmp/media.tgz', '~/tmp/media.tgz')
	with cd(env.dir):
		run('tar xzf ~/tmp/media.tgz')

# Get media remote --> local
@task
def get():
	with cd(env.dir):
		run('tar czf ~/tmp/media.tgz %s' % (env.media))
		get('~/tmp/media.tgz', '~/tmp/media.tgz')
		local('tar xzf ~/tmp/media.tgz')