#!/bin/bash
script_dir="$(cd "$(dirname "$0")" && pwd)"; folder="$script_dir/../data/aggregations"
tables=($(sqlite3 db.sqlite3 ".table"))
for file in "$folder"/*; do
    table="${file##*/}"; table="${table%.sql}"  # split the file so it has the same name as the table
    sqlite3 db.sqlite3 < $file
    echo "Table '$table' was just updated"
done