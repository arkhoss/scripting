#!/usr/bin/env python3
# Author: David Caballero <d@dcaballero.net>
# Version: 1.0
# Description: update api versions of kubeconfig
# Prerequisites:
#   Python 3.9+
#   pip3 install docopt
# !!!IMPORTANT make a backup of your kubeconfig file from ~/.kube/config
# before running this script!

"""

Usage:
  update-aws-kube-api.py [--path=<p>] [--debug] [--dry-run]
  update-aws-kube-api.py -h | --help | --version

Options:
  -h --help            Show this screen.
  -v --version         Show version.
  -p --path=<p>        Kubeconfig file path
  -r --debug           Debug mode, default false.
  -d --dry-run         Run without perform changes, default false.

"""

from docopt import docopt
from pathlib import Path
import subprocess, datetime, os, sys, time, yaml

def backup_kubeconfig(file_path):
    """
    """
    modified_time = os.path.getmtime(file_path) 
    time_stamp =  datetime.datetime.fromtimestamp(modified_time).strftime("%b-%d-%y-%H:%M:%S")
    subprocess.call("cp " + file_path + " " + file_path+"_"+time_stamp ,shell=True)
    return str(file_path+"_"+time_stamp)


def load_yaml(filename):
    """
    """
    try:
        print("Loading yaml file")
        with open(filename, "r") as read_file:
            loaded_file = yaml.safe_load(read_file)
            print("Yaml file loaded")
            if debug:
              print("Loaded File: " + str(loaded_file))
            return loaded_file
    except Exception as errors:
        raise errors


def kube_update(context,alias,profile,file_path):
    """
    """
    try:
        region = context["context"]["cluster"][12:21]
        cluster_name = context["context"]["cluster"].partition('/')[2]
        update_result = ''
        print("Updating cluster: " + cluster_name)
        if debug:
            print("update command: aws eks --region " + region + " update-kubeconfig --name "
                + cluster_name  + " --alias " + alias + " --profile " + profile + " --kubeconfig " + str(file_path) )
        if dry_run:
            print("Kubeconfig file not updated - dry_run enabled")
        else:
            update_result = subprocess.call(
                "aws eks --region " + region + " update-kubeconfig --name "
                + cluster_name  + " --alias " + alias + " --profile " + profile + " --kubeconfig " + file_path,
            shell=True,
            )
        if debug:
            print("Result update: " + str(update_result))
        if  update_result != 0:
            print("Cluster not updated... skipped")
            return "ClusterNotUpdated"
        return update_result
    except subprocess.CalledProcessError as errors:
        raise errors


def find_profile(cluster_arn, kubeconfig):
    """
    """
    try:
        users = kubeconfig["users"]
        user_name = ''
        profile = ''
        for i, user in enumerate(users):
            user_name = users[i]["name"]
            if user_name == cluster_arn:
                 value_profile = users[i]["user"]["exec"]["env"][0]["value"]
                 profile = value_profile
                 if debug:
                     print("Found Profile: " + str(profile))
        return profile
    except Exception as errors:
        raise errors


def main(arguments):
    home_path = str(Path.home())
    file_path = arguments['--path']
    filename = ''
    if debug:
        print("file_path: " + str(file_path) )
    if file_path == None:
        filename = os.path.join(home_path, ".kube/config")
    else:
        filename = os.path.join(home_path, file_path)

    if not dry_run:
        print("Backup kubeconfig file:" + backup_kubeconfig(filename))
    else:
        print("Kubeconfig file backup not created - dry_run enabled")

    kubeconfig = load_yaml(filename)

    contexts = kubeconfig["contexts"]

    alias = ''

    for i, context in enumerate(contexts):
        print("Context" + str(i))
        #print("Context content" + str(context) )
        alias = context["name"]
        cluster_arn = context["context"]["cluster"]
        if "aws" in cluster_arn:
            print("Updating Alias: " + alias )
            #kube_update(context,alias)
            profile = find_profile(cluster_arn,kubeconfig)
            print("profile:" + str(profile))
            update_result = kube_update(context,alias,profile,filename)
            print("Update: " + str(update_result))
        else:
            print("Not an AWS Cluster... skipped")



if __name__ == '__main__':
    arguments                = docopt(__doc__, version='1.0.0')
    dry_run                  = arguments['--dry-run']
    debug                    = arguments['--debug']
    main(arguments)
