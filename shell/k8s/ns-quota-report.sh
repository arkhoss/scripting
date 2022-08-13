#!/bin/bash

DATEUTC=`date -u +%Y%m%d`
NAMESPACES=$@

echo "Getting Namespaces Details..."
echo "namespace.name,limits.cpu_used,limits.cpu_hard,limits.memory_used,limits.memory_hard,persistentvolumeclaims_used,persistentvolumeclaims_hard,pods_used,pods_hard,px_ephemeral_used,px_ephemeral_hard,px_shared_used,px_shared_hard,px_standard_used,px_standard_hard,requests.cpu_used,requests.cpu_hard,requests.memory_used,requests.memory_hard" > k8snsdetails${DATEUTC}.csv

for i in $NAMESPACES;
do
    QUOTA=$(kubectl -n ${i} describe quota | awk 'NR>4')
    if [[ -z $QUOTA ]]; then
        continue
    fi
    
    echo -n "$i, "
    printf "%s\n" "$QUOTA" | while read property used hard;
    do
    echo -n "$used, $hard";
    if [ "$property" != "requests.memory" ]; then
        echo -n ","
    fi
    done;
echo ""
done >> k8snsdetails${DATEUTC}.csv
echo "Completed"

