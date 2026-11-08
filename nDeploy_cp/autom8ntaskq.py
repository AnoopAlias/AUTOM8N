from celery import Celery
import re
import subprocess
import yaml
import os

cpaneluser = os.environ["USER"]

app = Celery('autom8ntaskq', broker='redis://localhost:16380/0', backend="redis://localhost:16380/0")


@app.task
def regen_nginx_conf(cpaneluser):
    # SECURITY: username must be a plain cPanel account name; no shell interpolation.
    if not isinstance(cpaneluser, str) or not re.match(r'^[A-Za-z0-9][A-Za-z0-9_.-]*$', cpaneluser):
        return
    subprocess.call(['/opt/nDeploy/scripts/generate_config.py', cpaneluser])
    subprocess.call(['/usr/sbin/nginx', '-s', 'reload'])
