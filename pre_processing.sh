
# pre processing zip files with group names
find . -maxdepth 1 -name "*.zip" | while read -r file; do
    echo "Unzipping $file to folder"
    DIRNAME="${file%.zip}"
    if  find . -type d -name "$DIRNAME"; then
        echo "Removing old $DIRNAME folder"
        rm -rf "$DIRNAME"
    fi
    mkdir "$DIRNAME"
    unzip -O utf-8 -d "$DIRNAME" "$file"
done
