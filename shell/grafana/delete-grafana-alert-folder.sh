#!/bin/bash


GRAFANA_URL=$1
GRAFANA_TOKEN=$2
FOLDER_UID=$3

curl -s \
  -H "Authorization: Bearer ${GRAFANA_TOKEN}" \
  "${GRAFANA_URL}/api/v1/provisioning/alert-rules" |
jq -c --arg folder "$FOLDER_UID" '
  .[]
  | select(.folderUID == $folder or .folderUid == $folder)
  | {uid, provenance}
' |
while read -r rule; do
  uid=$(jq -r '.uid' <<< "$rule")
  provenance=$(jq -r '.provenance // "unknown"' <<< "$rule")

  echo "Deleting $uid (provenance=$provenance)"

  curl -sS \
    -X DELETE \
    -H "Authorization: Bearer ${GRAFANA_TOKEN}" \
    -H "X-Disable-Provenance: true" \
    "${GRAFANA_URL}/api/v1/provisioning/alert-rules/${uid}"

  echo
done
