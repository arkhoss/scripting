#!/usr/bin/env python3
# I'm moving away from argparse, so I used docopt which it is a cleaner argument parse package
# Tested in Gitlab EE 17.0.3
# Author: David Caballero <d@dcaballero.net>
# Version: 1.0
# Description: register runners
# This script leverages the GitLab REST API to register runners under a given user and generate the runner token
# https://docs.gitlab.com/ee/api/users.html#create-a-runner-linked-to-a-user
# It is capable of handling the GitLab rate-limiting logic, waiting until it is allowed to proceed.
# Prerequisites:
#   Python 3.9+
#   pip3 install datetime requests docopt
# For runner status https://docs.gitlab.com/ee/api/runners.html#list-all-runners

"""

Usage:
  register-runner.py (--url=<u>) (--token=<t>) (--runner-type=<r>) [--group-id=<g>] [--project-id=<p>] [--description=<d>] [--tag-list=<t>] [--debug] [--dry-run]
  register-runner.py -h | --help | --version

Options:
  -h --help            Show this screen.
  -v --version         Show version.
  -u --url=<u>         Gitlab URL i.e https://gitlab.com.
  -t --token=<t>       Gitlab personal user token.
  -r --runner-type=<r> Runner type Specifies the scope of the runner; instance_type, group_type, or project_type.
  -g --group-id=<g>    The ID of the group that the runner is created in. Required if runner_type is group_type.
  -p --project-id=<p>  The ID of the project that the runner is created in. Required if runner_type is project_type.
  -d --description=<d> Description of the runner.
  -t --tag-list=<t>    A list of runner tags.
  -r --debug           Debug mode, default false.
  -d --dry-run         Run without remove Runners, default false.

"""

from docopt import docopt
from requests.structures import CaseInsensitiveDict
import datetime, re, requests, sys, time

class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
    def writelines(self, datas):
        self.stream.writelines(datas)
        self.stream.flush()
    def __getattr__(self, attr):
        return getattr(self.stream, attr)

def wait_until(end_datetime):
    while True:
        diff = (end_datetime - datetime.datetime.now()).total_seconds()
        if diff < 0: return       # In case end_datetime was in past to begin with
        time.sleep(diff/2)
        if diff <= 0.1: return

def handle_response_rate_limit(r):
    remaining = r.headers.get('RateLimit-Remaining')
    if remaining is None:
        return
    if int(remaining) > 0:
        return

    print(f"Rate limit reached, waiting until {r.headers['RateLimit-ResetTime']}")
    wait_until(datetime.datetime.fromtimestamp(int(r.headers['RateLimit-Reset'])))

def register_runner(url, runner_type, group_id: None, project_id: None, tag_list: None, description: None):
    endpoint = ''

    if runner_type == 'group_type':
        endpoint = f'{url}/api/v4/user/runners?runner_type={runner_type}&group_id={group_id}'
    elif runner_type == 'project_type':
        endpoint = f'{url}/api/v4/user/runners?runner_type={runner_type}&project_id={project_id}'
    elif runner_type == 'instance_type':
        endpoint = f'{url}/api/v4/user/runners?runner_type={runner_type}'

    if tag_list is not None:
        endpoint = endpoint + f'&tag_list={tag_list}'
    
    if description is not None:
        endpoint = endpoint + f'&description={description}'

    if debug:
      print(f"POST {endpoint}")
    
    if dry_run:
        print(f" {endpoint}")
        return

    r = requests.post(endpoint, headers = headers)
    if debug:
      print(r.headers)
    
    handle_response_rate_limit(r)

    return r


def main(arguments):

    if dry_run:
        print('NOTE: Dry-run mode enabled')

    if debug:
        print('NOTE: Debug mode enabled')

    if debug:
        print(f"Registering runner...")

    r = register_runner(url, runner_type, group_id, project_id, tag_list, description)
    if r.status_code == 201:
        print(f"{r.json()['token']}")
    if r.status_code != 201:
        print(f"{r} ({r.reason})")
        exit(1)

if __name__ == '__main__':
    arguments                = docopt(__doc__, version='1.0.0')
    dry_run                  = arguments['--dry-run']
    debug                    = arguments['--debug']
    url                      = arguments['--url']
    runner_type              = arguments['--runner-type']
    group_id                 = arguments['--group-id']
    project_id               = arguments['--project-id']
    tag_list                 = arguments['--tag-list']
    description              = arguments['--description']
    headers                  = CaseInsensitiveDict()
    headers['Accept']        = 'application/json'
    headers['PRIVATE-TOKEN'] = arguments['--token']
    headers['User-Agent']    = 'register-runner.py'
    main(arguments)
