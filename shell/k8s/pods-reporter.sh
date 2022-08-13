#!/bin/bash

DATEUTC=`date -u +%Y%m%d`
NAMESPACES=$1

if [ -z $1 ]; then
    echo "Please specify a namespace \[\.\/pods\-reporter\.sh namespace\]"
fi

# Functions
echo "############# UTC TIME - `date -u` #############"
echo "Getting Namespaces Details..."
echo "namespace,prod_nodeselector,kn1,storage_kn1,kn2,storage_kn2,kn3,storage_kn3" > k8snspodreport${DATEUTC}.csv

for i in $NAMESPACES;
do
  # Number of pods per node
  pods=$(kubectl -n ${i} get po -o wide)
  if [ "${npods}" != 0 ]; then
  fi
done >> k8snspodreport${DATEUTC}.csv
echo "Completed"

