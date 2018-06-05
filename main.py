#!/usr/bin/env python

import argparse
from git import get_git_branch_name, create_pr, get_ticket_number, update_labels
from jira import make_jira_pr_body
from utils import open_git_pr_in_browser

parser = argparse.ArgumentParser()
parser.add_argument("-o", '--owner',
                    type=str, required=True, help="Name of project owner")
parser.add_argument("-p", '--project',
                    type=str, required=True, help="Name of project")
parser.add_argument("-a", '--api_token',
                    type=str, required=True, help="Git api token")
parser.add_argument("-hb", '--head_branch',
                    type=str, required=False, help="Head branch")
parser.add_argument("-l", '--label',
                    type=str, required=False, action='append', dest='labels', help="Label to apply to Pull Request")


args = parser.parse_args()

api_token = args.api_token
owner = args.owner
project = args.project
head_branch = args.head_branch
labels = args.labels

git_config = {
    'api_token': api_token,
    'owner': owner,
    'project': project,
    'base_branch': head_branch or 'development',
    'labels': labels
}

current_branch = get_git_branch_name()
ticket_number = get_ticket_number(current_branch)
body = make_jira_pr_body(ticket_number)

pr_number, pr_url = create_pr(branch_full_name=current_branch, body=body, **git_config)

update_labels(pr_number=pr_number, **git_config)

print('Pull request {number} created: {url}'.format(number=pr_number, url=pr_url))

open_git_pr_in_browser(pr_url)
