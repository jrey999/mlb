#!/bin/bash
folder="/Users/jreyno/home/professional/projects/mlb/data/schema"

for file in "$folder"/*; do
    sqlite3 mlb.sqlite3 < $file
done