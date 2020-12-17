#!/usr/bin/python3
#usage: config_tags_report.py [-h] [-p] [-r] [-c]
#optional arguments:
#  -h, --help            show this help message and exit
#  -p , --profile        AWS cli profile name
#  -r , --rule-name      AWS Config rule name
#  -c , --compliance-type
#                        AWS Config compliance type. The allowed values are
#                        COMPLIANT and NON_COMPLIANT .
# Author: David Caballero <d@dcaballero.net>
# Version: 1.0
# Description: generate a tags compliance report from Amazon Config Service

import logging
import boto3
import argparse
import sys
import json
import csv
from datetime import date
from botocore.exceptions import ClientError

########################
### Fixed Parameters ###
########################
LOG_FILENAME = 'config_tags_report.log'
DEFAULT_COLUMNS = ["account_id", "aws_region", "resource_id", "compliance_type", "resource_type", "tags"]
logging.basicConfig(filename=LOG_FILENAME, format="%(asctime)s %(message)s", level=logging.INFO)

########################
#### Main Code      ####
########################

# This gets the client with support for multiple profiles
# # if no profile is passed it will use default
def get_client(service, AWS_PROFILE):
    """
    Get AWS Client given a service and cli profile
    param: service - aws service for boto3 session
    param: AWS_PROFILE - aws cli profile in case of multiple account setup
    """
    logging.info("Creating the client for AWS profile: %s", AWS_PROFILE)
    try:
        if AWS_PROFILE:
            session = boto3.Session(profile_name=AWS_PROFILE)
            client = session.client(service)
        else: client = session.client(service)
    except ClientError as e:
        logging.error( "Could not connect to AWS due error: %s", e )

    return client


def get_resource_tags_by_id(client, resource_list):
    """
    Get Resources by ID and return a list of the resources with tags included
    param: client - aws client for config service
    param: resource_list - list of aws resources
    """
    logging.info("Gathering resource tags")

    resources_with_tags = []
    resource_tags = []

    try:
        if resource_list:
            for resource in resource_list:
                query = "SELECT resourceId,resourceName,resourceType,tags" \
                    " WHERE resourceType = '" + resource["resource_type"] + "'" \
                    " AND resourceId = '" + resource["resource_id"] + "'" \

                logging.debug("Running Amazon Config Resource Tags Query")
                logging.debug("tag query: %s", query)
                logging.debug("t_resourceid: %s", resource["resource_id"])

                if client.select_resource_config(Expression= query,Limit = 1)["Results"] == []:
                    logging.info("Resource does not exist")
                    continue
                else:
                    resource_tags = client.select_resource_config(
                        Expression= query,
                        Limit = 1
                    )["Results"][0]

                logging.debug("Query for tags was successful")
                resource_tags = json.loads(resource_tags)
                logging.debug("resource_tags: %s", resource_tags)
                if resource_tags is None:
                    logging.debug("resource_tags is none... damn")
                    break

                resource = {
                  "account_id": resource["account_id"],
                  "aws_region": resource["aws_region"],
                  "resource_id": resource["resource_id"],
                  "compliance_type": resource["compliance_type"],
                  "resource_type": resource["resource_type"],
                  "tags": resource_tags["tags"],
                }
                resources_with_tags.append(resource)
    except ClientError as e:
        logging.error( "Failed to run config query: %s", e )

    return resources_with_tags


def get_resources_from(compliance_details):
    """
    Get resources from client response with compliance details
    param: compliance_details - dict response from select_resource_config
    """
    resources = compliance_details["Results"]
    next_token = compliance_details.get("NextToken", None)

    return resources, next_token


def get_resources_compliance(client, rule_name, compliance_type):
    """
    Get rules compliance
    param: client - aws client for config service
    param: rule_name - name of rule to run the compliance query
    param: compliance_type - self explanatory
    """
    query = "SELECT accountId,awsRegion,configuration.targetResourceId,configuration.targetResourceType,configuration.complianceType,resourceType" \
              " WHERE resourceType = 'AWS::Config::ResourceCompliance'" \
              " AND configuration.complianceType = '" + compliance_type + "'" \
              " AND configuration.configRuleList.configRuleName = '" + rule_name + "'"

    resource_list = []

    try:
        logging.info("Running Amazon Config Resource Compliance Query")
        logging.debug("query: %s", query)

        next_token = ''
        resources = []

        while next_token is not None:
            compliance_details = client.select_resource_config(
                Expression= query,
                Limit=99,
                NextToken=next_token)
            current_batch, next_token = get_resources_from(compliance_details)
            resources += current_batch

        if resources:
            logging.debug("Query was successful")
            for resource in resources:
                resource = json.loads(resource)
                logging.debug("c_resource: %s", resource)
                logging.debug("c_resourceid: %s", resource["configuration"]["targetResourceId"])
                resource = {
                  "account_id": resource["accountId"],
                  "aws_region": resource["awsRegion"],
                  "resource_id": resource["configuration"]["targetResourceId"],
                  "compliance_type": resource["configuration"]["complianceType"],
                  "resource_type": resource["configuration"]["targetResourceType"]
                }
                resource_list.append(resource)
    except ClientError as e:
      logging.error( "Failed to run config query: %s", e )

    return resource_list


def write_csv(data, AWS_PROFILE):
    """
    Write the data into a csv report file with fixed columns
    param: data - list of data
    param: AWS_PROFILE - aws cli profile in case of multiple account setup
    """
    name = "config-tags-report-" + str(date.today()) + "-" + AWS_PROFILE + ".csv"
    logging.info("Creating .csv file: %s", name)
    try:
        with open(name, "w") as csvfile:
            writer = csv.DictWriter(csvfile, lineterminator="\n", fieldnames=DEFAULT_COLUMNS)
            writer.writeheader()
            for i in data:
                logging.debug("data row: %s", i)
                writer.writerow(i)
        logging.info("Created successfully: %s", name)
    except IOError:
        logging.error("IOError when writing the csv")



if __name__ == "__main__":

    try:
        parser = argparse.ArgumentParser("config_tags_report.py", add_help=True)
        parser.add_argument( '-p','--profile',default='default',dest='profile',action='store',metavar='',help='AWS cli profile name')
        parser.add_argument( '-r','--rule-name',default='default',dest='rule_name',action='store',metavar='',help='AWS Config rule name')
        parser.add_argument( '-c','--compliance-type',default='default',dest='compliance_type',action='store',metavar='',help='AWS Config compliance type. The allowed values are COMPLIANT and NON_COMPLIANT .')

        args = parser.parse_args()
        client = get_client("config", args.profile)
        resource_list = get_resources_compliance(client, args.rule_name, args.compliance_type)
        write_csv(get_resource_tags_by_id(client, resource_list), args.profile)
    except SystemExit:
        sys.exit(2)

