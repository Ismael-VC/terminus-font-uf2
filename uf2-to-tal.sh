#!/usr/bin/env sh

# File names
input_file="terminus.uf2"
temp_file="temp_hex.tal"
output_file="terminus.tal"

xxd -g 1 -c 16 "$input_file" | \
cut -d' ' -f2-17 | \
awk '{
    printf "%s %s %s %s %s %s %s %s  %s %s %s %s %s %s %s %s\n", \
    $1, $2, $3, $4, $5, $6, $7, $8, \
    $9, $10, $11, $12, $13, $14, $15, $16
}' > "$temp_file"

# Extract the first 256 bytes (16 lines * 16 bytes per line = 256 bytes)
head -n 16 "$temp_file" > "first_256_bytes.tal"
tail -n +17 "$temp_file" > "remaining_bytes.tal"

# Concatenate
echo "@font-terminus-mono-8x16" > "$output_file"
cat "first_256_bytes.tal" >> "$output_file"
echo "&glyphs" >> "$output_file"
cat "remaining_bytes.tal" >> "$output_file"

# Clean up
rm "$temp_file" "first_256_bytes.tal" "remaining_bytes.tal"

echo "Output saved to $output_file."
