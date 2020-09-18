from github import Github
import re


# TODO: Confirm this is working
def make_html_safe(s):
    s = re.sub(r'[^A-Za-z 0-9 \.,\?""!@#\$%\^&\*\(\)-_=\+;:<>\/\\\|\}\{\[\]`~]*', '', s)
    s = s.replace("&", '&amp;')
    s = s.replace("\"", '&quot;')
    s = s.replace(">", '&gt;')
    s = s.replace("<", '&lt;');
    return s


def print_single_issue(issue):
    line = f"<li><a href=\"{issue.html_url}\">{issue.number}</a> {make_html_safe(issue.title)}</li>"
    print(line)


def print_issues(issues, event_type: str, printed_ids: set):
    to_prints = []
    printed_count = 0
    for issue in issues:
        if issue.number not in printed_ids:
            to_prints.append(issue)
            printed_count += 1
            printed_ids.add(issue.number)
    if printed_count > 0:
        print(f"There are {printed_count} {event_type} tickets.")
        print("<ul>")
        [print_single_issue(i) for i in to_prints]
        print("</ul>")
    else:
        print(f"<p>There have been no {event_type.lower()} tickets.</p>")


g = Github()

repo = "geneontology/go-ontology"
# repo = "geneontology/amigo"
start_date = "2020-06-18"
new_issues = g.search_issues(query=f"repo:{repo} created:=>{start_date}")
# print(new_issues.totalCount)
updated_issues = g.search_issues(query=f"repo:{repo} updated:=>{start_date}")
# print(updated_issues.totalCount)

ids = set()
print_issues(new_issues, "New", ids)
print_issues(updated_issues, "Updated", ids)
