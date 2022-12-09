from celery import Celery
import subprocess, yaml, os

cpaneluser = os.environ["USER"]

app = Celery('autom8ntaskq', broker='redis://localhost:6379/0', backend="redis://localhost:6379/0")


@app.task
def regen_nginx_conf(cpaneluser):
    subprocess.call('/opt/nDeploy/scripts/generate_config.py '+cpaneluser, shell=True)
    subprocess.call('/usr/sbin/nginx -s reload', shell=True)
