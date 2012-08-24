from fabric.api import *
import logging

"""
Egregious virtualenv hackery for quick convenient deployment ensues...
"""


DEPLOY_DIR="/opt/jeevesbot"
LOCAL_JEEVESBOT_PATH=os.envirion['LOCAL_JEEVESBOT_PATH'] #TODO Handle this better...!

@task
def install_packages():
    packages = [
        'htop',
        'git',
        'python-virtualenv',
        'python-dev',
        'build-essential',
    ]
    
    package_list = ' '.join(packages)
    sudo("apt-get install %s" % package_list)
    sudo("pip install --upgrade pip virtualenv")

@task
def ensure_users():
    sudo("adduser jeevesbot || true")

@task
def prepare_for_jeevesbot():
    run("killall supervisord || true")
    sudo("rm -rf %s" % DEPLOY_DIR) # I can see myself regretting this in the future
    sudo("mkdir -p %s" % DEPLOY_DIR)
    with cd(DEPLOY_DIR):
        sudo("chown -R %s ." % env.user)
        run("virtualenv .")
        run("bin/pip install supervisor")
        run("bin/pip install importlib") # Sigh, Squeeze has 2.6; make this conditional (or just remove it when we get 2.7 tbh...)
        put("supervisord.conf", ".")
        run("bin/supervisord")
    
@task
def update_jeevesbot():
    put("%s/*" % LOCAL_JEEVESBOT_PATH, DEPLOY_DIR) #TODO Have this clone / pull?
    with cd(DEPLOY_DIR):
        run("bin/python setup.py develop")
    restart_jeevesbot()

@task
def restart_jeevesbot():
    run("%s/bin/supervisorctl restart jeevesbot" % DEPLOY_DIR)
