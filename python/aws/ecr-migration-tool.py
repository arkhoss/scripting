#!/usr/bin/python3
# Usage: usage: ecr_migration_tool.py [-h] [-p] [-O] [-r] -R
# required arguments:
#  -R , --registry AWS account id registry
# optional arguments:
#  -h, -help show this help message and exit
#  -p , --profile AWS cli profile name
#  -O , --old-registry Old on premise registry
#  -r , --region AWS region
# Author: David Caballero <d@dcaballero.net>
# Version: 1.0
# Description: move images from on-premise host to AWS ECR

import logging
import boto3
import argparse
import sys
import subprocess
from datetime import date
from botocore.exceptions import ClientError

########################
### Fixed Parameters ###
########################
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)

########################
#### Main Code      ####
########################

# Get local images
def get_local_images(registry, old_registry):
    logging.info("Getting local docker images")
    try:
        untagged_images = subprocess.check_output("docker image ls --format \"{{.Repository}}:{{.Tag}}\" | grep -v " + registry + "| grep " + old_registry, shell=True).splitlines()
    except subprocess.CalledProcessError as e:
        logging.error( "Could not get local docker images: %s", e )

    return untagged_images


# Set tags for local images with ECR Registry
def set_new_tags(registry, old_registry, region):
    logging.info("Starting tagging in local docker")

    registry_url = str(registry) + ".dkr.ecr." + str(region) + ".amazonaws.com/"
    images = get_local_images(registry, old_registry)

    commands = []
    tagged_images = []

    logging.info("Setting new tags in local docker")

    for image in images:
        temp_image = str(image.rsplit('/', 1)[-1])
        docker_cmd = "docker tag " + image + " " + registry_url + temp_image
        commands.append(docker_cmd)
        tagged_images.append(registry_url + temp_image)

    try:
        for command in commands:
            subprocess.call(command, shell=True)
    except subprocess.CalledProcessError as e:
        logging.error( "Could not tag local docker images: %s", e )

    return tagged_images


# This gets the client with support for multiple profiles
# # if no profile is passed it will use default
def get_client(service, AWS_PROFILE):

    try:
        if AWS_PROFILE:
            session = boto3.Session(profile_name=AWS_PROFILE)
            client = session.client(service)
        else: client = session.client(service)
    except ClientError as e:
        logging.error( "Could not connect to AWS due error: %s", e )

    return client


# Create ECR repositories
def create_ecr_repository(client, repo_name):

    logging.info("Creating a new repository at AWS ECR with name: %s", repo_name)

    try:
        client.create_repository(
            repositoryName=repo_name,
            imageScanningConfiguration={ 'scanOnPush': True }
        )
        logging.info("Repository Created!")
    except ClientError as e:
        logging.error( "Could not create repository at AWS ECR: %s", e )


# Push ECR repositories
def push_image(image_uri, image):

    logging.info("pusing image: %s", image)

    try:
        subprocess.check_output("docker push " + image_uri, shell=True)
        logging.info("Image push completed")
    except subprocess.CalledProcessError as e:
        logging.error( "Could not push image to ECR: %s", e )


# Push images to ECR repositories
def push_ecr_images(profile, registry, old_registry, region):

    logging.info("Creating the client for AWS profile: %s", profile)

    client = get_client('ecr', profile)

    registry_url = str(registry) + ".dkr.ecr." + str(region) + ".amazonaws.com/"
    images = get_local_images(registry, old_registry)

    # docker login
    try:
        subprocess.check_output(
            "aws ecr get-login-password --region " + region +
            " | docker login --username AWS --password-stdin " +
            str(registry) + ".dkr.ecr." + str(region) + ".amazonaws.com",
            shell=True )
        logging.info("AWS ECR Login Succeeded")
    except subprocess.CalledProcessError as e:
        logging.error( "Could not push image to ECR: %s", e )

    for image in images:
        image_uri = registry_url + str(image.rsplit('/', 1)[-1])
        temp_image = str(image.rsplit('/', 1)[-1]).rsplit(':', 1)[0]

        logging.info("Check if ECR repository exist for image: %s", temp_image)

        try:
            client.describe_repositories(
                registryId=registry,
                repositoryNames=[ temp_image, ]
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'RepositoryNotFoundException':
                create_ecr_repository(client, temp_image)
                push_image(image_uri, temp_image)
            else:
                logging.error( "Error found: %s", e )
        else:
            push_image(image_uri, temp_image)


if __name__ == "__main__":

    try:
        parser = argparse.ArgumentParser("ecr_migration_tool.py", add_help=True)
        parser.add_argument( '-p','--profile',default='default',dest='profile',action='store',metavar='',help='AWS cli profile name')
        parser.add_argument( '-O','--old-registry',default='\'\'', dest='old_registry',action='store',metavar='',help='Old on premise registry')
        parser.add_argument( '-r','--region',default='us-east-1',dest='region',action='store',metavar='',help='AWS region')
        parser.add_argument( '-R','--registry',dest='registry',action='store',metavar='',help='AWS account id registry', required=True)

        args = parser.parse_args()
        set_new_tags(args.registry, args.old_registry, args.region)
        push_ecr_images(args.profile, args.registry, args.old_registry, args.region)

    except SystemExit:
        sys.exit(2)

