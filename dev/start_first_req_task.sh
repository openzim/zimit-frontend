echo "Retrieving access token"

ZF_ADMIN_TOKEN="$(curl -s -X 'POST' \
    'http://localhost:8004/v2/auth/authorize' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{"username":"admin","password":"admin"}' \
    | jq -r '.access_token')"

echo "Get last requested task"

LAST_TASK_ID="$(curl -s -X 'GET' \
  'http://localhost:8004/v2/requested-tasks' \
  -H 'accept: application/json' \
  -H "Authorization: Bearer $ZF_ADMIN_TOKEN" \
  | jq -r '.items[0]._id')"

if [ "$LAST_TASK_ID" = "null" ]; then
    echo "No pending requested task. Exiting script."
    exit 1
fi

echo "Start task"

curl -s -X 'POST' \
  "http://localhost:8004/v2/tasks/$LAST_TASK_ID?worker_name=worker" \
  -H 'accept: application/json' \
  -H "Authorization: Bearer $ZF_ADMIN_TOKEN" \
  -d ''

echo "DONE"
