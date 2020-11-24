#!/bin/sh

JS_PATH=/usr/share/nginx/html/environ.js
echo "dump ZIM* environ variables to $JS_PATH"

json_output="var environ = {\n"
for envLine in $(env)
do
    if [ "$(echo "$envLine" | cut -c1-3)" = "ZIM" ]; then
        ns=$(echo "$envLine" | sed 's/=/": "/')
        json_output="$json_output    \"$ns\",\n"
    fi
done
json_output="$json_output}\n"
# shellcheck disable=SC2039
printf "$json_output" > $JS_PATH

cat $JS_PATH
echo "-----"

exec "$@"
