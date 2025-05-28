# BMW PID Data Project

This project provides structured C header files containing BMW engine PID (Parameter ID) data, auto-generated from CSV data sources. The PID data was originally sourced from [thesecretingredient.neocities.org/bmw/](https://thesecretingredient.neocities.org/bmw/). It is designed to help developers and engineers integrate, analyze, or visualize BMW engine diagnostic data in C or C++ projects.

## Features
- **CSV to C Struct Conversion**: Converts BMW PID CSV files into C header files with struct arrays for direct use in C/C++ code.
- **Auto-Generated Headers**: Each engine type (e.g., N55, B48, B58, N63, S55, S63) has a corresponding header file (e.g., `n55_pid_data.h`).
- **Consistent Struct Format**: All PID entries are represented as arrays of structs, making them easy to iterate and use programmatically.
- **Python Automation Script**: Includes a script (`csv_to_struct_header.py`) to automate the conversion process for any compatible CSV file.
- **Version Controlled**: All files are managed in a git repository for easy tracking and collaboration.

## File Structure
- `*.csv` — Raw BMW PID data for each engine type.
- `*.h` — Auto-generated C header files containing struct arrays for each engine type.
- `csv_to_struct_header.py` — Python script to convert CSV files to C header files.
- `bmw_pid_scrapper.py` — (Optional) Additional script for scraping or processing PID data.

## Usage
1. **Convert CSV to Header**: Run the Python script to generate or update header files:
   ```sh
   python3 csv_to_struct_header.py
   ```
   This will process all `*_pid_data.csv` files in the directory and generate corresponding `*_pid_data.h` files.

2. **Include in C/C++ Project**: Include the generated header files in your C or C++ project:
   ```c
   #include "n55_pid_data.h"
   // ...
   for (size_t i = 0; i < N55_PID_DATA_DATA_COUNT; ++i) {
       // Access n55_pid_data_data[i]
   }
   ```

## Struct Format Example
Each header file defines a struct and an array, e.g.:
```c
typedef struct {
    unsigned int pid;
    const char * description;
    const char * units;
    const char * data_type;
    double multiply;
    double divide;
    double add;
} n55_pid_data_entry;

static const n55_pid_data_entry n55_pid_data_data[] = {
    {0x4201, "Ambient pressure", "hPa", "unsigned integer", 0.0390625, 1, 0},
    // ...
};
#define N55_PID_DATA_DATA_COUNT (sizeof(n55_pid_data_data)/sizeof(n55_pid_data_data[0]))
```

## Data Source Credit
BMW PID data was originally sourced from [thesecretingredient.neocities.org/bmw/](https://thesecretingredient.neocities.org/bmw/).

## License
This project is provided as-is for educational and development purposes. See individual file headers for additional information.

---
*Auto-generated README. For questions or contributions, please open an issue or pull request.*
