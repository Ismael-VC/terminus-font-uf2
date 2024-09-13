#!/usr/bin/env sh

input_file="terminus.uf2"
temp_file="temp_hex.tal"
output_file="terminus.tal"

xxd -g 1 -c 16 "$input_file" | \
cut -d' ' -f2-17 | \
awk '{
    printf "%s%s %s%s %s%s %s%s  %s%s %s%s %s%s %s%s\n", \
    $1, $2, $3, $4, $5, $6, $7, $8, \
    $9, $10, $11, $12, $13, $14, $15, $16
}' > "$temp_file"

head -n 8 "$temp_file" > "first_128_bytes.tal"
tail -n +82 "$temp_file" > "remaining_bytes.tal"

echo "@font-terminus" > "$output_file"
cat "first_128_bytes.tal" >> "$output_file"
echo "&glyphs" >> "$output_file"
cat "remaining_bytes.tal" >> "$output_file"

awk '{
    if (/0000 0000 0000 0000  0000 0000 0000 0000/) {
        count++;
        if (count == 1 || count == 2) {
            print;
            next
        }
        last = $0
    } else {
        print
    }
}
END {
    if (count > 2) print last
}' "$output_file" > "$temp_file"

sed '106,210d' "$temp_file" > "$output_file"

rm "$temp_file" "first_128_bytes.tal" "remaining_bytes.tal"

echo "Output saved to $output_file."
