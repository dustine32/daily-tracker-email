import re
import requests
import json
import datetime
import argparse
import smtplib
from email.message import EmailMessage

parser = argparse.ArgumentParser()
parser.add_argument('repo_name')
parser.add_argument('duration_in_days')


# TODO: Confirm this is working
def make_html_safe(s):
    s = re.sub(r'[^A-Za-z 0-9 \.,\?""!@#\$%\^&\*\(\)-_=\+;:<>\/\\\|\}\{\[\]`~]*', '', s)
    s = s.replace("&", '&amp;')
    s = s.replace("\"", '&quot;')
    s = s.replace(">", '&gt;')
    s = s.replace("<", '&lt;')
    return s


def print_single_issue(issue):
    line = f"<li><a href=\"{issue['html_url']}\">{issue['number']}</a> {make_html_safe(issue['title'])}</li>"
    return line


def print_issues(issues, event_type: str, printed_ids: set):
    to_prints = []
    printed_count = 0
    text_output = ""
    ul_open = "<ul>"
    ul_close = "</ul>"
    for issue in issues:
        if issue["number"] not in printed_ids:
            to_prints.append(issue)
            printed_count += 1
            printed_ids.add(issue["number"])
    event_header = f"<h3>{event_type} Tickets</h3>"
    text_output = add_to_body(text_output, event_header)
    if printed_count > 0:
        ticket_count_header = f"There are {printed_count} {event_type.lower()} tickets."
        text_output = add_to_body(text_output, ticket_count_header)
        text_output = add_to_body(text_output, ul_open)
        [print_single_issue(i) for i in to_prints]
        for i in to_prints:
            text_output = add_to_body(text_output, print_single_issue(i))
        text_output = add_to_body(text_output, ul_close)
    else:
        ticket_count_header = f"<p>There have been no {event_type.lower()} tickets.</p>"
        text_output = add_to_body(text_output, ticket_count_header)
    return text_output


def get_issues(repo: str, event_type: str, start_date: str):
    url = f"https://api.github.com/search/issues?q=repo:{repo}+{event_type}:=>{start_date}&type=Issues&per_page=100"
    resp = requests.get(url)
    if resp.status_code == 200:
        resp_objs = json.loads(resp.content)
        issues = resp_objs.get("items", [])
        return issues
    else:
        raise Exception(f"HTTP error status code: {resp.status_code} for url: {url}")


def add_to_body(current_body: str, text_to_add: str):
    current_body = "{}\n{}".format(current_body, text_to_add)
    return current_body


if __name__ == "__main__":
    # repo = "geneontology/go-ontology"
    # repo = "geneontology/amigo"
    args = parser.parse_args()
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(int(args.duration_in_days))

    body = ""

    new_issues = get_issues(args.repo_name, "created", yesterday)
    updated_issues = get_issues(args.repo_name, "updated", yesterday)

    summary_header = f"<h2>Summary for tickets from {yesterday} to {today}</h2>"
    body = add_to_body(body, summary_header)
    ids = set()
    body = add_to_body(body, print_issues(new_issues, "New", ids))
    body = add_to_body(body, print_issues(updated_issues, "Updated", ids))

    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = "GitHub {} Tracker Update".format(args.repo_name)
    msg["From"] = "go-admin@usc.edu"
    msg["To"] = "debert@usc.edu"

    s = smtplib.SMTP('email.usc.edu', port=587)
    s.send_message(msg)
    s.quit()
