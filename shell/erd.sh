output_file="data/schema/schema.sql"
folder="data/schema/tables"

# Remove existing output file
rm -f "$output_file"

# Loop through each file in the folder
for file in "$folder"/*; do
    cat "$file" >> "$output_file"  # Append file content to output file
done

echo "Files combined into $output_file"