import requests
import subprocess
from json import dumps

GIT_API_URL = 'https://api.github.com/repos/{owner}/{project}/pulls'


def create_pr(branch_full_name,
              body,
              api_token,
              owner,
              project,
              base_branch):

    data = dumps({
        "title": branch_full_name.replace('_', ' ').replace('-', ' '),
        "body": body,
        "head": branch_full_name,
        "base": base_branch
    })

    url = GIT_API_URL.format(owner=owner, project=project)
    header = {'Authorization': 'token {api_token}'.format(api_token=api_token)}

    response = requests.post(url, data=data, headers=header)

    if response.status_code == 200:
        return response.json().get('html_url')

    raise Exception(response.json().get('message'))


def open_git_pr_in_browser(href):
    subprocess.call(['/usr/bin/open', href])


def get_git_branch_name():
    git_get_current_branch = 'git rev-parse --abbrev-ref HEAD'.split(' ')
    return subprocess.check_output(git_get_current_branch).decode("utf-8")


def get_ticket_number(branch_full_name):
    return '-'.join(branch_full_name.split('-')[0:2])


JIRA_URL = 'https://administrate.atlassian.net/browse/{ticket_number}'


def make_jira_pr_body(branch_full_name):
    ticket_number = get_ticket_number(branch_full_name)
    return JIRA_URL.format(ticket_number=ticket_number)