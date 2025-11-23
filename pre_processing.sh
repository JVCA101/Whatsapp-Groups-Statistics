
# pre processing zip files with group names
find . -maxdepth 1 -name "*.zip" | while read -r file; do
    echo "Unzipping $file to folder"
    DIRNAME="${file%.zip}"
    if ! find . -type d -name "$DIRNAME"; then
        mkdir "$DIRNAME"
    fi
    unzip -d "$DIRNAME" "$file"
done
