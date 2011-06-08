from fabric.api import local, settings, cd, run, env
from fabric.colors import green


REPO_URL = "git://github.com/jpgneves/hojehatransportes.git"

env.user = "hagreve"

def _deploy(path):
    # with settings(warn_only=True):
    #     local("python manage.py schemamigration hat --auto")
    # local("git add hat/migrations/*.py")
    # with settings(warn_only=True):
    #     local("git commit -m '[Fabric] Added new migrations'")
    # local("git push")
    with settings(warn_only=True):

        # REPO
        if run("test -d %s/repo" % path).failed:
            print(green("Cloning repo."))
            run("git clone %s %s/repo" % (REPO_URL, path))

        # Link to the relevant folder on the repo
        if run("test -d %s/hojehatransportes" % path).failed:
            print(green("Linking hojehatransportes to folder in repo."))
            run("ln -s %s/repo/hojehatransportes %s/hojehatransportes" % (path, path))

        # copy settings from 'root'
        if run("test -f %s/hojehatransportes/settings.py" % path).failed:
            print(green("Copying settings file."))
            run("cp %s/settings.py %s/hojehatransportes" % (path, path))

    # update files and restart
    with cd("%s/hojehatransportes" % path):
        print(green("Updating repo, migrating and restarting."))
        run("git pull")
        with settings(warn_only=True):
            run("python manage.py syncdb")
            run("python manage.py migrate hat")
        run("touch %s/tmp/restart.txt" % path)
        print(green("All done."))

def deploy_to_testing():
    path = '/home/hagreve/test.hagreve.com'
    _deploy(path)

def deploy_to_production():
    path = '/home/hagreve/hagreve.com'
    _deploy(path)


def howto():
    print("To run on remote server:\n\tfab -H hagreve.com deploy_to_[testing|production]")