#!/usr/bin/env python3
# Author: David Caballero <d@dcaballero.net>
# Inspired by Eric Paul
# Version: 1.0
# Description: route53 record importer to export in tf, tg or csv
# Prerequisites:
#   Python 3.9+
#   pip3 install docopt boto3 requests requests-aws4auth

"""

Usage:
  r53-record-importer.py get-records --zone=<z> [--profile=<p>] [--debug] [--dry-run]
  r53-record-importer.py generate-records --zone=<z> [--output-format=<o>] [--filter=<f>] [--profile=<p>] [--debug] [--dry-run]
  r53-record-importer.py import-records --zone=<z> [--iac-command=<i>] [--filter=<f>] [--profile=<p>] [--debug] [--dry-run]
  r53-record-importer.py -h | --help | --version

Options:
  -h --help              Show this screen.
  -v --version           Show version.
  -z --zone=<z>          Hosted zone id
  -i --iac-command=<i>   IAC command to run [tg,tf], default tf
  -o --output-format=<o> Output format [csv,tg], default csv
  -f --filter=<f>        Filter records by name, default all
  -p --profile=<p>       AWS profile [default: default]
  --debug                Debug mode, default false.
  --dry-run              Run without perform changes, default false.

"""

import os
import csv
import sys
import json
import boto3
import logging
import subprocess
from docopt import docopt
from pathlib import Path
from datetime import date
from botocore.exceptions import ClientError
from jinja2 import Environment, FileSystemLoader

#from requests_aws4auth import AWS4Auth
#import subprocess, datetime, os, sys, time, yaml


def get_client(service, AWS_PROFILE):
    """
    Get an AWS Client for a specific service with or without profile
    """
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


def write_csv(data, report_name):
    """
    Write data to a csv file
    """
    name = report_name + "-" + str(date.today()) + ".csv"
    logging.info("Creating .csv file: %s", name)
    try:
        with open(name, "w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=DEFAULT_COLUMNS)
            writer.writeheader()
            for key, value in data.items():
                logging.debug("data row: %s", value)
                data = dict(zip(DEFAULT_COLUMNS,data))
                writer.writerow(value)
        logging.info("Created successfully: %s", name)
    except IOError:
        logging.error("IOError when writing the csv")


def run_process(command, print_stderr=True):
    """
    Run a shell command in a subprocess.
    """
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if stderr and print_stderr:
        logging.info(f'[ stderr ]: {stderr.decode("utf-8")}')

    return stdout


def print_command(command):
    """
    Print a command
    """
    command_string = ' '.join(command)
    logging.info(f'++ {command_string}')


def unicode_decode(text):
    """
    Decode ACII and unicoded strings.
    """
    return bytes(text, 'utf-8').decode('unicode_escape')


def get_all_records_list(hosted_zone, profile, client):
    """
    Get list of all records of a given zone
    """

    records_list = []

    record_set = client.list_resource_record_sets(HostedZoneId=hosted_zone)
    records_list.extend(record_set['ResourceRecordSets'])

    while record_set['IsTruncated']:
        next_record_name = record_set['NextRecordName']
        record_set = client.list_resource_record_sets(
            HostedZoneId=hosted_zone,
            StartRecordName=next_record_name
        )
        records_list.extend(record_set['ResourceRecordSets'])

    logging.debug(records_list)

    return records_list


def include_record(record, zone_name):
    """
    Determine whether or not to include a record in an import.
    """
    if record['Type'] == 'NS' and record['Name'] == zone_name:
        return False

    if record['Type'] == 'SOA':
        return False

    if 'TrafficPolicyInstanceId' in record:
        return False

    return True


def get_record_map(record_list, zone_name, record_filter=None):
    """
    Create an indexable map/dict of records for import.
    """
    records_map = {}
    for record in record_list:
        if include_record(record, zone_name):
            record_type = record['Type']

            if record_type in ('TXT', 'SPF') and 'ResourceRecords' in record:
                for resource in record['ResourceRecords']:
                    resource['Value'] = resource['Value'].strip('"')

            record_id = unicode_decode(record['Name']).rstrip('.')
            record_id += f'_{record_type}'

            if 'SetIdentifier' in record:
                set_id = record['SetIdentifier']
                record_id += f'_{set_id}'

            if record_filter is not None:
                if record_filter in record_id:
                    records_map[record_id] = record
            else:
                records_map[record_id] = record

    return records_map


def record_is_alias(record):
    """
    Determine if a route53 record is an AWS alias record.
    """
    return 'AliasTarget' in record

def get_imports(record_list, hosted_zone, zone_info, iac_command):
    """
    Get a list of import template objects and commands for route53 records in a zone.
    """
    objects = []
    commands = []
    zone_name = zone_info['HostedZone']['Name'].rstrip('.')


    for key, record in record_list.items():
        dns_type    = record['Type']
        dns_name    = record['Name']
        zone_name   = unicode_decode(dns_name).rstrip('.')
        record_type = 'records' if not record_is_alias(record) else 'alias'

        objects.append(
            f'resource "aws_route53_record" "{record_type}[{key}]" {{}}'
        )

        object_id = f'{hosted_zone}_{zone_name}_{dns_type}'
        if 'SetIdentifier' in record:
            set_id = record['SetIdentifier']
            object_id += f'_{set_id}'

        commands.append([
            iac_command, 'import',
            f'aws_route53_record.{record_type}["{key}"]',
            object_id
        ])

    return objects, commands


def build_geolocation_args(data):
    """
    Build geolcation arguments for terraform/terragrunt template.
    """
    geoloc = {}

    if 'ContinentCode' in data:
        geoloc['continent'] = data['ContinentCode']

    if 'CountryCode' in data:
        geoloc['country'] = data['CountryCode']

    if 'SubdivisionCode' in data:
        geoloc['subdivision'] = data['SubdivisionCode']

    return geoloc


def replace_last(subject, search, replace, occurrences):
    """
    Replace the last N occurrences of a substring.
    """
    list_items = subject.rsplit(search, occurrences)
    return replace.join(list_items)


def extract_common_values(rec, zone_name):
    """
    Extract fields common to value records and aliases.
    """
    record_name = unicode_decode(rec['Name'])

    common = {
        'name':   record_name,
        'type':   rec['Type'],
        'prefix': replace_last(record_name, zone_name, '', 1).rstrip('.')
    }

    if 'HealthCheckId' in rec:
        common['health_check_id'] = rec['HealthCheckId']

    if 'SetIdentifier' in rec:
        common['set_identifier'] = rec['SetIdentifier']

    if 'Weight' in rec:
        common['routing_weight'] = rec['Weight']

    if 'Region' in rec:
        common['routing_latency_region'] = rec['Region']

    if 'GeoLocation' in rec:
        common['routing_geolocation'] = build_geolocation_args(rec['GeoLocation'])

    if 'Failover' in rec:
        common['routing_failover'] = rec['Failover']

    if 'MultiValueAnswer' in rec and rec['MultiValueAnswer']:
        common['multivalue_answer_routing_policy'] = True

    return common


def get_tf_template_args(zone_info, record_map, module_source_path):
    """
    Get template arguments to build terragrunt.hcl for a recordset.
    """
    zone_name = zone_info['HostedZone']['Name'].rstrip('.')
    private_zone = zone_info['HostedZone']['Config']['PrivateZone']
    template_args = {
        'module_source': f'{module_source_path}/route53-records',
        'zone_name':     zone_name,
        'private_zone':  private_zone
    }

    if private_zone:
        template_args['vpc_id'] = zone_info['VPCs'][0]['VPCId']

    records = {}
    aliases = {}
    for key, rec in record_map.items():
        record_values = []
        common_values = extract_common_values(rec, zone_name)

        if 'ResourceRecords' in rec:
            # This is a resource record with address information.
            for value in rec['ResourceRecords']:
                record_values.append(value['Value'])

            records[key] = {
                'ttl':    rec['TTL'],
                'values': record_values,
            }
            records[key].update(common_values)

        else:
            # This is an alias record.
            aliases[key] = {
                'evaluate_target_health': rec['AliasTarget']['EvaluateTargetHealth'],
                'alias_name':             rec['AliasTarget']['DNSName'],
                'zone_id':                rec['AliasTarget']['HostedZoneId']
            }
            aliases[key].update(common_values)

    template_args['records'] = records
    template_args['aliases'] = aliases

    return template_args


def generate_tg_records(zone_record_list, zone_info, record_map, report_name):
    logging.info("Generating tg records...")

    name = report_name + "-" + str(date.today()) + ".hcl"

    logging.info("Creating terragrunt file: %s", name)
    try:
        logging.info("Writing terragrunt file.")
        base_path = os.path.dirname(os.path.realpath(__file__))
        file_loader = FileSystemLoader(f'{base_path}/_templates')

        env = Environment(loader=file_loader)
        env.trim_blocks = True
        env.lstrip_blocks = True

        template = env.get_template('records.terragrunt.hcl.j2')
        tf_template_args = get_tf_template_args(zone_info, record_map, base_path)

        output = template.render(tf_template_args)

        with open(name, 'w') as f:
            f.write(output)

    except IOError:
        logging.error("IOError when writing the csv")

    for record in zone_record_list:
        logging.debug(json.dumps(record, indent=2))


def generate_csv_records(zone_record_list):
    write_csv(zone_record_list, "records")

def generate_records(zone_record_list, hosted_zone, zone_info, output, record_filter=None):
    record_map = get_record_map(zone_record_list, hosted_zone, record_filter)
    logging.debug("records map")
    logging.debug(json.dumps(record_map, indent=2))
    if output == "tg":
        generate_tg_records(zone_record_list, zone_info, record_map, "records")
    else:
        logging.info("Generating csv records...")
        generate_csv_records(record_map)


def generate_imports(zone_record_list, hosted_zone, zone_info, iac_command, record_filter=None):
    record_map = get_record_map(zone_record_list, hosted_zone, record_filter)

    if iac_command == "tg":
        iac_command = 'terragrunt'
    else:
        iac_command = 'terraform'

    import_objects, import_commands = get_imports(record_map, hosted_zone, zone_info, iac_command)

    if dry_run:
        logging.info("Generating import commands")
        logging.info(json.dumps(import_commands))
        logging.info("Generating import objects")
        logging.info(json.dumps(import_objects))
    else:
        if debug:
            logging.debug("Generating import commands")
            logging.debug(json.dumps(import_commands))
            logging.debug("Generating import objects")
            logging.debug(json.dumps(import_objects))
        else:
            logging.info("Initializing %s.", iac_command)
            logging.info(run_process([iac_command, 'init', '-reconfigure']).decode("utf-8"))
            logging.info("Running RECORDSET import.")
            for cmd in import_commands:
                print_command(cmd)
                OUTPUT = run_process(cmd)
                logging.info(OUTPUT.decode('utf-8'))


def main(arguments):
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
    logging.debug("arguments: " + str(arguments))
    hosted_zone = arguments.get('--zone')
    profile = arguments.get('--profile')

    client    = get_client('route53', profile)
    zone_info = client.get_hosted_zone(Id=hosted_zone)
    zone_name = zone_info['HostedZone']['Name'].rstrip('.')
    logging.info("Hosted Zone Name: %s", zone_name)

    zone_record_list = get_all_records_list(hosted_zone, profile, client)

    if dry_run:
        logging.info("Running in dry-mode no changes will be performed")

    if debug:
        logging.debug("Debug mode enabled, no changes will be performed by the script")
    if arguments.get('get-records'):
        if debug:
            logging.info("Getting all Records for the hosted zone %s", zone_name)
            logging.info("ZONE RECORDS: ")
            logging.debug(json.dumps(zone_record_list, indent=2))
        else:
            logging.info("Getting all Records for the hosted zone %s", zone_name)
            logging.info("ZONE RECORDS: ")
            logging.info(json.dumps(zone_record_list, indent=2))

    if arguments.get('generate-records'):
        logging.info("Generate all records for the hosted zone %s", zone_name)
        if debug:
            logging.info("ZONE RECORDS: ")
            logging.info(json.dumps(zone_record_list, indent=2))
        if arguments.get('--filter') is not None:
            generate_records(zone_record_list, zone_name, zone_info, arguments.get('--output-format'), arguments.get('--filter'))
        else:
            generate_records(zone_record_list, zone_name, zone_info, arguments.get('--output-format'))

    if arguments.get('import-records'):
        logging.info("Import all Records for the hosted zone %s", zone_name)
        if debug:
            logging.info("ZONE RECORDS: ")
            logging.info(json.dumps(zone_record_list, indent=2))

        generate_imports(zone_record_list, hosted_zone, zone_info, arguments.get('--iac-command'), arguments.get('--filter'))


if __name__ == '__main__':
    logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)
    arguments                = docopt(__doc__, version='1.0.0')
    DEFAULT_COLUMNS          = ["Name", "Type", "TTL", "ResourceRecords", "AliasTarget"]
    dry_run                  = arguments['--dry-run']
    debug                    = arguments['--debug']
    main(arguments)
