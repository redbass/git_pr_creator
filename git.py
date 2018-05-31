import requests
from requests.exceptions import HTTPError
import subprocess
from json import dumps

GIT_API_CREATE_PR_URL = 'https://api.github.com/repos/{owner}/{project}/pulls'
GIT_API_ADD_LABEL_URL = 'https://api.github.com/repos/{owner}/{project}/issues/{pr_number}/labels'
JIRA_URL = 'https://administrate.atlassian.net/browse/{ticket_number}'


def create_pr(branch_full_name,
              body,
              api_token,
              owner,
              project,
              base_branch,
              labels):

    data = dumps({
        "title": branch_full_name.replace('_', ' ').replace('-', ' '),
        "body": body,
        "head": branch_full_name,
        "base": base_branch
    })

    url = GIT_API_CREATE_PR_URL.format(owner=owner, project=project)
    header = {'Authorization': 'token {api_token}'.format(api_token=api_token)}

    try:
        response = requests.post(url, data=data, headers=header)
        response.raise_for_status()
    except HTTPError as e:
        if not e.response:
            raise
        message = e.response.json().get('message')
        raise Exception(str(e) + '. Message: ' + message)

    response_data = response.json()
    html_url = response_data.get('html_url')
    pr_number = response_data.get('number')
    if isinstance(labels, list) and len(labels) > 0:
        add_label_url = GIT_API_ADD_LABEL_URL.format(owner=owner, project=project, pr_number=pr_number)
        requests.post(add_label_url, data=dumps(labels), headers=header)

    return pr_number, html_url


def open_git_pr_in_browser(href):
    subprocess.call(['/usr/bin/open', href])


def get_git_branch_name():
    git_get_current_branch = 'git rev-parse --abbrev-ref HEAD'.split(' ')
    return subprocess.check_output(git_get_current_branch) \
        .decode("utf-8").replace('\n', '')


def get_ticket_number(branch_full_name):
    return '-'.join(branch_full_name.split('-')[0:2])


def make_jira_pr_body(branch_full_name):
    ticket_number = get_ticket_number(branch_full_name)
    return JIRA_URL.format(ticket_number=ticket_number)
