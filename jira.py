JIRA_URL = 'https://administrate.atlassian.net/browse/{ticket_number}'


def make_jira_pr_body(ticket_number):
    return JIRA_URL.format(ticket_number=ticket_number)