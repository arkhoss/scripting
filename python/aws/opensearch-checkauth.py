#!/usr/bin/env python3
# Author: David Caballero <d@dcaballero.net>
# Version: 1.0
# Description: check access with Role for opensearch aws
# Prerequisites:
#   Python 3.9+
#   pip3 install docopt boto3 requests requests-aws4auth

"""

Usage:
  opensearch-checkauth.py cat --query=<q> --host=<H> --region=<r> [--debug] [--dry-run]
  opensearch-checkauth.py -h | --help | --version

Options:
  -h --help              Show this screen.
  -v --version           Show version.
  -q --query=<q>         Opensearch query
  -H --host=<H>          Host URL of opensearch endpoint, must include https:// and trailing /
  -r --region=<r>        AWS region.
  --debug                Debug mode, default false.
  --dry-run              Run without perform changes, default false.

"""

import json
import boto3
import requests
from docopt import docopt
from pathlib import Path
from requests_aws4auth import AWS4Auth
#import subprocess, datetime, os, sys, time, yaml

def queries(host, query, awsauth):
    """
        Register a repository for Opensearch snapshots
    """
    path = query
    url = host + path

    if debug:
        print(url)

    headers = {"Content-Type": "application/json"}

    if dry_run:
        print("dry run enabled, cat nodes command will run if dry run disabled.")
    else:
        r = requests.get(url, auth=awsauth, headers=headers)
        print(r.status_code)
        print(r.text)


# TODO: (dcaballero) add some functions to patch opensearch backend roles
#def addRole():
#    """
#        Register a role for Opensearch backend roles
#    """
#    path = '_snapshot/' + repo_name
#    url = host + path
#
#    if debug:
#        print(url)
#
#    payload = {
#      "type": "s3",
#      "settings": {
#          "bucket": bucket_name,
#          "region":  region,
#          "role_arn":  role_arn
#      }
#    }
#
#    if debug:
#        print(payload)
#
#    headers = {"Content-Type": "application/json"}
#
#    if dry_run:
#        print("dry run enabled, Register repo command will run if dry run disabled.")
#    else:
#        r = requests.put(url, auth=awsauth, json=payload, headers=headers)
#        print(r.status_code)
#        print(r.text)



def main(arguments):
    print("arguments: " + str(arguments))
    host = arguments['--host']
    region = arguments['--region']
    query = arguments['--query']
    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
    if debug:
        print("Debug mode enabled, no changes will be performed by the script")
    if query != None:
        print(queries(host, query, awsauth))


if __name__ == '__main__':
    arguments                = docopt(__doc__, version='1.0.0')
    dry_run                  = arguments['--dry-run']
    debug                    = arguments['--debug']
    main(arguments)
