#!/usr/bin/env python3
# Author: David Caballero <d@dcaballero.net>
# Version: 1.0
# Description: register repo, take snapshots and restore snapshots for opensearch aws
# Prerequisites:
#   Python 3.9+
#   pip3 install docopt boto3 requests requests-aws4auth

"""

Usage:
  opensearch-snapshots.py register-repo --host=<H> --region=<r> --bucket-name=<b> --repo-name=<n> --role-arn=<ra> [--debug] [--dry-run]
  opensearch-snapshots.py snapshot new --host=<h> --region=<r> --repo-name=<n> --snapshot-name=<s> [--debug] [--dry-run]
  opensearch-snapshots.py snapshot restore --host=<h> --region=<r> --repo-name=<n> --snapshot-name=<s> [--debug] [--dry-run]
  opensearch-snapshots.py snapshot restore-index --host=<h> --region=<r> --repo-name=<n> --snapshot-name=<s> --index-name=<i> [--debug] [--dry-run]
  opensearch-snapshots.py -h | --help | --version

Options:
  -h --help              Show this screen.
  -v --version           Show version.
  -H --host=<H>          Host URL of opensearch endpoint, must include https:// and trailing /
  -r --region=<r>        AWS region.
  -b --bucket-name=<b>   S3 Bucket name to store the snapshot.
  -n --repo-name=<n>     Name of the repository to store or retreive snapshots.
  -ra --role-arn=<ra>    ARN of the IAM Role with access to the snapshots repo.
  -s --snapshot-name=<s> Name of the snapshot to store or retreive.       
  -i --index-name=<i>    Name of the index to be restored.
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

def register_repo(host, repo_name, bucket_name, region, role_arn, awsauth):
    """
        Register a repository for Opensearch snapshots
    """
    path = '_snapshot/' + repo_name
    url = host + path

    if debug:
        print(url)

    payload = {
      "type": "s3",
      "settings": {
          "bucket": bucket_name,
          "region":  region,
          "role_arn":  role_arn
      }
    }

    if debug:
        print(payload)

    headers = {"Content-Type": "application/json"}
    
    if dry_run:
        print("dry run enabled, Register repo command will run if dry run disabled.")
    else:
        r = requests.put(url, auth=awsauth, json=payload, headers=headers)
        print(r.status_code)
        print(r.text)


def take_snapshot(host, repo_name, snapshot_name, awsauth):
    """
        Take opensearch snapshot
    """
    
    path = '_snapshot/' + repo_name + '/' + snapshot_name
    url = host + path

    if debug:
        print(url)


    if dry_run:
        print("dry run enabled, take snapshot command will run if dry run disabled.")
    else:
        r = requests.put(url, auth=awsauth)
        print(r.text)


def delete_index(host, index_name):
    """
        Delete index
    """
    
    path = index_name
    url = host + path

    if debug:
        print(url)

    if dry_run:
        print("dry run enabled, delete index command will run if dry run disabled.")
    else:
        r = requests.delete(url, auth=awsauth)
        print(r.text)
    

def restore_snapshot(repo_name, snapshot_name):
    """
        Restore snapshot (all indexes except Dashboards and fine-grained access control)
    """
    
    path = '_snapshot/' + repo_name + '/' + snapshot_name + '/_restore'
    url = host + path

    if debug:
        print(url)

    payload = {
      "indices": "-.kibana*,-.opendistro_security",
      "include_global_state": False
    }

    if debug:
        print(payload)

    headers = {"Content-Type": "application/json"}

    if dry_run:
        print("dry run enabled, restore snapshot command will run if dry run disabled.")
    else:
        r = requests.post(url, auth=awsauth, json=payload, headers=headers)
        print(r.text)


def restore_snapshot_index(repo_name, snapshot_name, index_name):
    """
        Restore snapshot (one index)
    """
    
    path = '_snapshot/' + repo_name + '/' + snapshot_name + '/_restore'
    url = host + path

    if debug:
        print(url)

    payload = {"indices": index_name}

    if debug:
        print(payload)

    headers = {"Content-Type": "application/json"}

    if dry_run:
        print("dry run enabled, restore snapshot command will run if dry run disabled.")
    else:
        r = requests.post(url, auth=awsauth, json=payload, headers=headers)
        print(r.text)


def main(arguments):
    print("arguments: " + str(arguments))
    host = arguments['--host']
    region = arguments['--region']
    repo_name = arguments['--repo-name'] 
    bucket_name = arguments['--bucket-name'] 
    role_arn = arguments['--role-arn'] 
    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
    if debug:
        print("Debug mode enabled, no changes will be performed by the script")
    if arguments['register-repo']:
        print("Registering a repository for snaptshots under Opensearch")
        register_repo(host, repo_name, bucket_name, region, role_arn, awsauth)
    if arguments['snapshot'] and arguments['new']:
        print("Creating  a new snapshot...")
        take_snapshot(host, repo_name, arguments['--snapshot-name'], awsauth)
    if arguments['restore']:
        print("Restoring all indexes under snapshopt except dashboard and opensearch security")
        restore_snapshot(repo_name, arguments['--snapshot-name'])
    if arguments['restore-index']:
        print("Resoring specific index under snapshot")
        restore_snapshot_index(repo_name, arguments['--snapshot-name'], arguments['--index-name'])


if __name__ == '__main__':
    arguments                = docopt(__doc__, version='1.0.0')
    dry_run                  = arguments['--dry-run']
    debug                    = arguments['--debug']
    main(arguments)
