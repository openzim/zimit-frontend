echo "Retrieving access token"

ZF_ADMIN_TOKEN="$(curl -s -X 'POST' \
    'http://localhost:8002/v2/auth/authorize' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{"username":"admin","password":"admin"}' \
    | jq -r '.access_token')"


echo "Worker check-in (will create if missing)"

curl -s -X 'PUT' \
  'http://localhost:8002/v2/workers/worker/check-in' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $ZF_ADMIN_TOKEN" \
  -d '{
  "username": "admin",
  "cpu": 3,
  "memory": 1024,
  "disk": 0,
  "offliners": [
    "zimit"
  ]
}'

echo "DONE"
