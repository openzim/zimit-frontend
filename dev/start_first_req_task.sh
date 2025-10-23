#!/bin/bash

die() {
    echo "ERROR: $1" >&2
    exit 1
}

check_http_code() {
    local http_code="$1"
    local response="$2"

    if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
	:
    else
	error_msg=$(echo "$response" | jq -r '.errors // .message // .detail // "Unknown error"' 2>/dev/null || echo "HTTP $http_code")
	die "Could not checkin worker: ${error_msg}"
    fi
}

echo "Retrieving access token"

ZF_ADMIN_TOKEN="$(curl -s -X 'POST' \
    'http://localhost:8004/v2/auth/authorize' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{"username":"admin","password":"admin"}' \
    | jq -r '.access_token')"

if [ -z "$ZF_ADMIN_TOKEN" ] || [ "$ZF_ADMIN_TOKEN" = "null" ]; then
    die "Failed to retrieve admin access token"
fi

echo "Get last requested task"

LAST_TASK_ID="$(curl -s -X 'GET' \
  'http://localhost:8004/v2/requested-tasks' \
  -H 'accept: application/json' \
  -H "Authorization: Bearer $ZF_ADMIN_TOKEN" \
  | jq -r '.items[0].id')"

if [ "$LAST_TASK_ID" = "null" ]; then
    die "No pending requested task. Exiting script."
fi

echo "Start task"

response=$(curl -s -w "\n%{http_code}" -X 'POST' \
  "http://localhost:8004/v2/tasks/$LAST_TASK_ID?worker_name=test_worker" \
  -H 'accept: application/json' \
  -H "Authorization: Bearer $ZF_ADMIN_TOKEN" \
)
http_code=$(echo "$response" | tail -n1)

check_http_code "$http_code"

echo "DONE"
