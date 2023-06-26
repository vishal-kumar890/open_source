
from subprocess import Popen, PIPE, run


def solve_task(conn,user_id,filename,download_url,download_path):
    download_video(download_url+filename,download_path)

def download_video(video_link,video_folder):
    run([r"/usr/bin/wget", video_link],cwd=video_folder)

