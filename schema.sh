#!/bin/bash
folder="$(dirname "$0")/data/schema"

for file in "$folder"/*; do
    sqlite3 mlb.sqlite3 < $file
done