#!/bin/bash

# Load JSON configuration
config_file="config.json"

# Extract variables and construct the variables string
variables=$(jq -r '
    def flatten: . as $in | 
        reduce (path(..) | select(type == "array" and length == 2)) as $p (
            {}; . * getpath($p) as $v | if $v | type == "object" 
            then {} else { ($p | join(".")): $v } end
        );
    .work.variables | flatten | to_entries | 
    map("\(.key)=\(.value|tostring)") | join(",")
' "$config_file")

# Run the databricks bundle command
databricks bundle run --var="$variables"
