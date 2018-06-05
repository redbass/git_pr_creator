import subprocess


def open_git_pr_in_browser(href):
    subprocess.call(['/usr/bin/open', href])