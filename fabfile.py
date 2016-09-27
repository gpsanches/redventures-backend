from fabric.api import cd, task, local, run, prefix, lcd, path
# from fabvenv import virtualenv
import os


# PROJECT_DIR = "/opt/redventures/redventures-backend"
# VENV = "/opt/redventures/venv/bin/activate"

PROJECT_DIR = "/Users/gsanches/Projects/python/redventures"
VENV = "/Users/gsanches/Projects/python/env/redventures/bin/"

LOG_DIR = "/var/log/redventures-test"
LOG_PATH = "{0}/application.log".format(LOG_DIR)


@task
def remove_cache():
    """
    Removes python cache files(.pyc) and folders(__pycache__).
    :return:
    """
    print("...Removing caching files")
    local('find . | egrep "*.pyc|__pycache__|celerybeat*" | sudo xargs rm -rf')
    print("......Caching files have been removed!\n")


@task
def create_log_dir():
    """
    Creates dir and file. Gives permission to write.
    :return:
    """
    if not os.path.isdir(LOG_DIR):
        print("...Creating log dir and log file in {0}".format(LOG_DIR))
        local("sudo mkdir {0}".format(LOG_DIR))
        local("sudo chmod 775 {0}".format(LOG_DIR))
        local("sudo touch {0}".format(LOG_PATH))
        local("sudo chmod 777 {0}".format(LOG_PATH))

    if not os.path.exists(LOG_PATH):
        print("...Creating log file in {0}".format(LOG_PATH))
        local("sudo touch {0}".format(LOG_PATH))
        local("sudo chmod 777 {0}".format(LOG_PATH))


@task
def start_app():
    local('git pull origin master')
    local('pip freeze')
    local('pip install -r requirements.txt')
    local('which python')
    local("python api_rest.py --module=widgetsspa --port=8888")


@task
def deploy():
    """
    Deploys application.
    :return:
    """
    with lcd(PROJECT_DIR):
        remove_cache()
        create_log_dir()
        start_app()
