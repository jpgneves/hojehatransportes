from fabric.api import local, settings, cd, run, env
import fabric.colors


REPO_URL = "git://github.com/jpgneves/hojehatransportes.git"

env.user = "hagreve"

def _deploy(path, branch):
    print(fabric.colors.green("Deploying branch %s into %s" % (branch, path)))
    
    with settings(warn_only=True):
        local("python manage.py schemamigration hat --auto")
    local("git add hat/migrations/*.py")
    with settings(warn_only=True):
        local("git commit -m '[Fabric] Added new migrations'")
    local("git push")
    with settings(warn_only=True):

        # REPO
        if run("test -d %s/repo" % path).failed:
            print(fabric.colors.green("Cloning repo."))
            run("git clone -b branch %s %s/repo" % (REPO_URL, path))

        # Link to the relevant folder on the repo
        if run("test -d %s/hojehatransportes" % path).failed:
            print(fabric.colors.green("Linking hojehatransportes to folder in repo."))
            run("ln -s %s/repo/hojehatransportes %s/hojehatransportes" % (path, path))

        # copy settings from 'root'
        if run("test -f %s/hojehatransportes/settings.py" % path).failed:
            print(fabric.colors.green("Copying settings file."))
            run("cp %s/settings.py %s/hojehatransportes" % (path, path))

    # update files and restart
    with cd("%s/hojehatransportes" % path):
        print(fabric.colors.green("Updating repo, migrating and restarting."))
        run("git checkout %s" % branch)
        run("git pull")
        with settings(warn_only=True):
            run("python manage.py syncdb")
            run("python manage.py migrate hat")
        run("touch %s/tmp/restart.txt" % path)
        print(fabric.colors.green("All done."))

def deploy_to_testing(branch="-"):
    path = '/home/hagreve/test.hagreve.com'
    if branch == "-":
        branch = getBranch()
    _deploy(path, branch)

def deploy_to_production():
    path = '/home/hagreve/hagreve.com'
    branch = 'master'
    _deploy(path, branch)


def howto():
    print("To run on remote server:\n\tfab -H hagreve.com deploy_to_[testing|production]")


def getBranch():
    return local('git branch | grep "*" | sed -e "s/^\* //"', capture=True)