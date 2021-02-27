import json
import requests
from ..settings import SENTRY_URL


SENTRY_API_TOKEN = '0cf91b8cd7b14cd1906d5b463a38e664f086a67c9e104b72a272f488d6a23118'

organization_slug = 'sentry'


def get_issue_list(project_slug):
    # api_url = f'{SENTRY_URL}/api/0/projects/{organization_slug}/{project_slug}/issues/?statsPeriod=14d'
    api_url = f'{SENTRY_URL}/api/0/projects/{organization_slug}/{project_slug}/issues/'
    headers = {
        'Authorization': f'Bearer {SENTRY_API_TOKEN}',
    }
    response = requests.get(api_url, headers=headers)
    return response


def get_event_list(project_slug):
    # api_url = f'{SENTRY_URL}/api/0/projects/{organization_slug}/{project_slug}/issues/?statsPeriod=14d'
    api_url = f'{SENTRY_URL}/api/0/projects/{organization_slug}/{project_slug}/events/'
    headers = {
        'Authorization': f'Bearer {SENTRY_API_TOKEN}',
    }
    response = requests.get(api_url, headers=headers)
    return response


def delete_issue(issue_id):
    api_url = f'{SENTRY_URL}/api/0/issues/{issue_id}/'
    headers = {
        'Authorization': f'Bearer {SENTRY_API_TOKEN}',
    }
    response = requests.delete(api_url, headers=headers)
    return response


if __name__ == '__main__':
    # for i in range(1, 1000):
        r = get_event_list('sender')
        data = json.loads(r.text)
        for row in data:
            print(row)
            # issue_id = row['permalink'].split('/')[-2]
            # print(issue_id)
            # rr = delete_issue(issue_id)
            # print(rr.status_code, rr.text)
