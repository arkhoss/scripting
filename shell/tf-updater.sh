#!/bin/bash

# safe pipefail
set -euo pipefail

# terraform version
_tfVERSION=$1

# download terraform
sudo wget https://releases.hashicorp.com/terraform/${_tfVERSION}/terraform_${_tfVERSION}_linux_amd64.zip

# setup steps
if [ ! -d /opt/terraform/ ]; then
   sudo mkdir -p /opt/terraform/
fi

sudo unzip -o terraform_${_tfVERSION}_linux_amd64.zip -d /opt/terraform/

if [ ! -f /usr/bin/terraform ]; then
   sudo ln -sv /opt/terraform/terraform /usr/bin
fi

echo "terraform version is now"
terraform -v

sudo rm -rf terraform_${_tfVERSION}_linux_amd64.zip
