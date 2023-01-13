#!/usr/bin/python3
# Usage: iam_user_creds_report.py [-p] <profile-name>
# Author: David Caballero <d@dcaballero.net>
# Version: 1.0
# Description: generates a report about iam users key usage

import logging
import boto3
import csv
import sys
import argparse
from datetime import date
from botocore.exceptions import ClientError

####################
# Fixed Parameters #
####################
DEFAULT_COLUMNS = ["user_name", "user_key_id", "last_usage_detail"]

#############
# Main Code #
#############

# This gets the client with support for multiple profiles
# if no profile is passed it will use default
def get_client(service, AWS_PROFILE):
    try:
        if AWS_PROFILE:
            session = boto3.Session(profile_name=AWS_PROFILE)
            client = session.client(service)
        else:
            client = boto3.client(service)
    except ClientError as e:
        logging.error(
            "Could not connect to AWS due error: %s", e
        )
    return client

# This get a list of all users
def get_all_users_list(client):

    list_to_return = []
    list = client.list_users()

    while True:
        for user in list['Users']:
            list_to_return.append(user)
        else:
            break
    return list_to_return

# this get usage details of each key of each user
def get_user_key_last_used_date(profile):

    user_key_details = []

    client = get_client('iam', profile)
    all_users_list = get_all_users_list(client)

    for user in all_users_list:

        user_name = user['UserName']

        access_keys = client.list_access_keys(UserName=user_name)["AccessKeyMetadata"]

        message = {}

        if access_keys:
            for access_key in access_keys:
                access_key_id = access_key["AccessKeyId"]
                access_key_status = access_key["Status"]

                last_used_date = client.get_access_key_last_used(
                    AccessKeyId=access_key_id
                ).get("AccessKeyLastUsed").get("LastUsedDate")

                if access_key_status == "Inactive":
                    message = {
                        "user_name": user_name,
                        "user_key_id": access_key_id,
                        "last_usage_detail": "KEY_INACTIVE",
                    }
                elif access_key_status == "Active" and last_used_date is None:
                    message = {
                        "user_name": user_name,
                        "user_key_id": access_key_id,
                        "last_usage_detail": "KEY_NEVER_USED",
                    }
                else:
                    message = {
                        "user_name": user_name,
                        "user_key_id": access_key_id,
                        "last_usage_detail": last_used_date,
                    }
                user_key_details.append(message)
        else:
            message = {
                "user_name": user_name,
                "user_key_id": "none",
                "last_usage_detail": "User do not have any active access key.",
            }
            user_key_details.append(message)
    return user_key_details

# this save the results in a csv file
def write_csv(data, profile):
    name = "iam-user-report" + str(date.today()) + "-" + profile + ".csv"
    logging.info("Creating .csv file: %s", name)
    try:
        with open(name, "w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=DEFAULT_COLUMNS)
            writer.writeheader()
            for i in data:
                writer.writerow(i)
        logging.info("Created successfully: %s", name)
    except IOError:
        logging.error("IOError when writing the csv")


if __name__ == "__main__":

    try:
        parser = argparse.ArgumentParser("Generates a report about iam users key usage")
        parser.add_argument(
            '-p',
            '--profile',
            default='default',
            dest='profile',
            action='store',
            metavar = '',
            help='aws cli profile')

        args = parser.parse_args()
        write_csv(get_user_key_last_used_date(args.profile), args.profile)
        print( "Report Completed")
    except SystemExit:
        sys.exit(2)


