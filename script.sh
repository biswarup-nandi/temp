#!/bin/bash

# Load JSON configuration
config_file="config.json"

# Extract variables and construct the variables string
variables=$(jq -r '.work.variables | to_entries | map(.key + "=" + (if .value | type == "object" then (.value | to_entries | map(.key + "=" + (.value | tostring)) | join(",")) else (.value | tostring) end)) | join(",")' "$config_file")

# Run the databricks bundle command
databricks bundle run --var="$variables"
