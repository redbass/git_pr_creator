import argparse
from git import get_git_branch_name, create_pr, \
    open_git_pr_in_browser, make_jira_pr_body

parser = argparse.ArgumentParser()
parser.add_argument("-o", '--owner',
                    type=str, required=True, help="Name of project owner")
parser.add_argument("-p", '--project',
                    type=str, required=True, help="Name of project")
parser.add_argument("-a", '--api_token',
                    type=str, required=True, help="Git api token")
parser.add_argument("-hb", '--head_branch',
                    type=str, required=False, help="Head branch")


args = parser.parse_args()

git_config = {
    'api_token': args.api_token,
    'owner': args.owner,
    'project': args.project,
    'base_branch': args.head_branch or 'development'
}

current_branch = get_git_branch_name()
body = make_jira_pr_body(current_branch)
pr_url = create_pr(branch_full_name=current_branch, body=body, **git_config)
open_git_pr_in_browser(pr_url)
