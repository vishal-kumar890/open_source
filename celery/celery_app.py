import os
from . import main_run as mr
from celery import Celery, current_task
from dotenv import load_dotenv
from .sqlConnector import sqlConnect


load_dotenv()

broker_url = os.getenv('celery_url')
if not broker_url:
    raise AssertionError("No broker URL")

oci_download_url = os.getenv('oci_download_url')

if not oci_download_url:
    raise AssertionError("No Video download URL")

file_download_path = os.getenv('file_download_path')

if not file_download_path:
    raise AssertionError("No file download path given")

if not os.path.isdir(file_download_path):
    os.makedirs(file_download_path)

main_db = os.getenv('db_name')
if not main_db:
    raise AssertionError("No database")

if not os.path.isfile(main_db):
    raise AssertionError("Not valid database path")



celery_app = Celery('tasks', broker=broker_url, backend='rpc://')
celery_app.control.purge()
celery_app.conf.update(task_track_started=True)


@celery_app.task(name="solve_task", acks_late=True)
def verify_model(user_id,filename):
    with sqlConnect(main_db) as conn:
        mr.solve_task(conn, user_id,filename,oci_download_url,file_download_path)


