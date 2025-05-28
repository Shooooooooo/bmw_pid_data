import os
import csv
import re

# Directory containing the CSV files
dir_path = os.path.dirname(os.path.abspath(__file__))

# Map CSV column names to C struct field names and types
def get_struct_fields(header):
    # Map for known columns
    mapping = [
        ("PID", "unsigned int", "pid"),
        ("Description", "const char *", "description"),
        ("Units", "const char *", "units"),
        ("Data Type", "const char *", "data_type"),
        ("Multiply", "double", "multiply"),
        ("Divide", "double", "divide"),
        ("Add", "double", "add"),
    ]
    fields = []
    for col, ctype, cname in mapping:
        if col in header:
            fields.append((ctype, cname, header.index(col)))
    return fields

def sanitize_string(s):
    # Escape quotes and backslashes for C
    return s.replace('\\', r'\\').replace('"', r'\"')

def csv_to_header(csv_path):
    base = os.path.splitext(os.path.basename(csv_path))[0]
    h_path = os.path.join(dir_path, base + ".h")
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        fields = get_struct_fields(header)
        # Use the common struct from bmw_pid_entry.h
        struct_name = 'bmw_pid_entry'
        array_name = base + '_data'
        count_macro = base.upper() + '_DATA_COUNT'
        # Write header file
        with open(h_path, 'w', encoding='utf-8') as out:
            out.write(f"// Auto-generated from {os.path.basename(csv_path)}\n")
            out.write(f"#ifndef {base.upper()}_H\n#define {base.upper()}_H\n\n")
            out.write(f"#include <stddef.h>\n")
            out.write(f"#include \"bmw_pid_entry.h\"\n\n")
            # No struct definition here, just use the common one
            # Array definition
            out.write(f"static const {struct_name} {array_name}[] = {{\n")
            for row in reader:
                if not row or row[0].startswith('//'):
                    continue
                values = []
                for ctype, cname, idx in fields:
                    val = row[idx].strip()
                    if ctype == 'unsigned int' or ctype == 'double':
                        values.append(val)
                    elif ctype == 'const char *':
                        values.append(f'\"{sanitize_string(val)}\"')
                    else:
                        values.append(val)
                out.write('    {' + ', '.join(values) + '},\n')
            out.write(f"}};\n\n")
            out.write(f"#define {count_macro} (sizeof({array_name})/sizeof({array_name}[0]))\n\n")
            out.write(f"#endif // {base.upper()}_H\n")

if __name__ == "__main__":
    for fname in os.listdir(dir_path):
        if fname.endswith('.csv'):
            csv_to_header(os.path.join(dir_path, fname))
