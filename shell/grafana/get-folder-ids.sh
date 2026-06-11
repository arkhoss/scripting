#!/bin/bash

GRAFANA_URL=$1
GRAFANA_TOKEN=$2

curl -s \
  -H "Authorization: Bearer ${GRAFANA_TOKEN}" \
  -H "Content-Type: application/json" \
  "${GRAFANA_URL}/api/folders" | jq
