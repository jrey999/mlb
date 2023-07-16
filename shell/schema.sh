#!/bin/bash
script_dir="$(cd "$(dirname "$0")" && pwd)"; folder="$script_dir/../data/schema/tables"
tables=($(sqlite3 mlb.sqlite3 ".table"))
for file in "$folder"/*; do
    table="${file##*/}"; table="${table%.sql}"  # split the file so it has the same name as the table
    # Check if the table exists
    if [[ " ${tables[*]} " == *" $table "* ]]; then
    echo "Table '$table' has already been created"
    else
        sqlite3 mlb.sqlite3 < $file
        echo "Table '$table' was just created"
    fi
done
YEAR=$(date +"%Y")
sqlite3 mlb.sqlite3 <<-EOF
    INSERT INTO
        season
    (
        season_id, season_start, playoffs_start
    )
SELECT
    $YEAR, game_date,
(
    SELECT
        MAX(game_date) + (12 * 60 * 60) -- Adding 12 hours in seconds
    FROM
        game
)
FROM
    game
WHERE
    strftime('%Y', game_date) = $YEAR
ORDER BY
    game_date
LIMIT 1
    ON CONFLICT(season_id)
    DO UPDATE SET
season_start = excluded.season_start,
season_end = excluded.playoffs_start;

EOF