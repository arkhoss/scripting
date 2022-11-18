#!/usr/bin/env python3
# Inspired by https://gitlab.com/-/snippets/2150325 by Pedro Pombeiro
# I'm moving away from argparse, so I used docopt which it is a cleaner argument parse package
# Also modified the rest call to be from all runners instead of just single runners endpoint
# Tested in Gitlab EE 15.3.3
# Author: David Caballero <d@dcaballero.net>
# Version: 1.0
# Description: Prune offline gitlab runners
# This script leverages the GitLab REST API to enumerate all owned offline runners (which haven't contacted the GitLab instance for at least 2 hours) / not_connected runners (which have never contacted the GitLab instance) and optionally delete them.
# It is capable of handling the GitLab rate-limiting logic, waiting until it is allowed to proceed.
# Prerequisites:
#   Python 3.9+
#   pip3 install datetime requests docopt
# For runner status https://docs.gitlab.com/ee/api/runners.html#list-all-runners

"""

Usage:
  cleanup-runners.py (--url=<u>) (--token=<t>) [--status=<s>] [--debug] [--dry-run]
  cleanup-runners.py -h | --help | --version

Options:
  -h --help            Show this screen.
  -v --version         Show version.
  -u --url=<u>         Gitlab URL i.e https://gitlab.com.
  -t --token=<t>       Gitlab personal user token.
  -s --status=<s>      Gitlab Runner status to filter, default offline.
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

def rest_get_runners(filter, url, page=1):
    endpoint = f'{url}/api/v4/runners/all?{filter}&per_page=100&page={page}'
    if debug:
      print(f"GET {endpoint}")

    r = requests.get(endpoint, headers = headers)
    if debug:
      print(r.headers)

    return r

def rest_delete_runners(ids, url):
    r = None

    for id in ids:
        endpoint = f'{url}/api/v4/runners/{id}'
        if debug:
            print(f"DELETE {endpoint}")
        r = requests.delete(endpoint, headers = headers)
        if r.status_code != 204:
            print(f"{id}: {r} ({r.reason})")
        if debug:
            print(r.headers)
        else:
            print('.', end = '')
        handle_response_rate_limit(r)

    if not debug:
        print('')

    return r

def delete_runners(ids, url):
    if len(ids) == 0:
        return

    if dry_run:
        print(f"Would delete {len(ids)} runners ({ids})...")
        return

    print(f"Deleting {len(ids)} runners ({ids})...")

    stdoutSave = sys.stdout
    sys.stdout = Unbuffered(sys.stdout)
    r = rest_delete_runners(ids, url)
    sys.stdout = stdoutSave

def main(arguments):

    status = arguments['--status']

    if arguments['--status'] == None:
        status = 'offline'

    runners_filter = f"status={status}"


    if dry_run:
        print('NOTE: Dry-run mode enabled')

    total = 0
    page = 1

    print(f"Retrieving first page...", end = ' - ')
    r = rest_get_runners(runners_filter, url, page = page)
    if r.status_code != 200:
        print(f"{r} ({r.reason})")
        exit(1)

    total_pages = countdown_pages = int(r.headers['X-Total-Pages'])
    print("total pages found: ",total_pages )
    print("next page value first value: ", r.headers['X-Next-Page'])
    if int(r.headers['X-Total']) == 0:
        print('No runners retrieved. Please make sure that the status filter is set accordingly and that the authentication token has permissions for the intended runners')
        exit(0)

    while True:
        nodes = r.json()
        if len(nodes) == 0:
            break

        total = total + len(nodes)
        ids = []
        for node in nodes:
            ids.append(node['id'])

        handle_response_rate_limit(r)

        if dry_run:
            print(f'running dry mode skipping delete runners step')
            print(f'runner to be deleted ids', ids)
        else:
            print(f'deleting runners...')
            print(f'runner ids', ids)
            delete_runners(ids, url)

        print(f"Retrieving new page, { countdown_pages - 1} pages remaining...", end = ' - ')

        if page == total_pages:
            print(f'No more pages')
            print(f'Reached end of list, processed {total} runners')
            break

        r = rest_get_runners(runners_filter,url, page = page)
        page += 1
        if dry_run:
            print(f'Next page is: ', page)

        if dry_run:
            countdown_pages = countdown_pages - (page - 1)

if __name__ == '__main__':
    arguments                = docopt(__doc__, version='1.0.0')
    dry_run                  = arguments['--dry-run']
    debug                    = arguments['--debug']
    url                      = arguments['--url']
    status                   = arguments['--status']
    headers                  = CaseInsensitiveDict()
    headers['Accept']        = 'application/json'
    headers['PRIVATE-TOKEN'] = arguments['--token']
    headers['User-Agent']    = 'cleanup-runners.py'
    main(arguments)
