from fabric.api import local, settings, cd, run, env

REPO_URL = "git://github.com/jpgneves/hojehatransportes.git"

env.user = "hagreve"

def _deploy(path):
    local("python manage.py schemamigration hat --auto")
    local("git add hat/migrations/*.py")
    local("git commit -m '[Fabric] Added new migrations'")
    local("git push")
	with settings(warn_only=True):
		if run("test -d %s" % path).failed:
			run("git clone %s %s" % (REPO_URL, path))
	with cd(path):
		run("git pull")
		run("python manage.py migrate hat")
		run("touch %s/../tmp/restart.txt" % path)

def deploy_to_testing():
	path = '/home/hagreve/test.hagreve.com/hojehatransportes'
	_deploy(path)

def deploy_to_production():
	path = '/home/hagreve/hagreve.com/hojehatransportes'
	_deploy(path)