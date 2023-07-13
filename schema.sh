#!/bin/bash
folder="$(dirname "$0")/data/schema"

for file in "$folder"/*; do
    tablename="${file##*/}"
    tablename="${tablename%.sql}"  # Remove the ".sql" extension to get the table name
    
    # Check if the table exists
    if sqlite3 your_database.db ".table $tablename" &>/dev/null; then
        echo "Table $tablename already exists"
    else
        sqlite3 db.sqlite3 < $file
        echo "Table $tablename has been created"
    fi
done