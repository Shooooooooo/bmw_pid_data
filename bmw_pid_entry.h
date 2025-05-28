#ifndef BMW_PID_ENTRY_H
#define BMW_PID_ENTRY_H

#ifdef __cplusplus
extern "C" {
#endif

// Common struct for all BMW PID CSV files
// Columns: PID, Description, Units, Data Type, Multiply, Divide, Add

typedef struct {
    unsigned int pid;
    const char *description;
    const char *units;
    const char *data_type;
    double multiply;
    double divide;
    double add;
} bmw_pid_entry;

#ifdef __cplusplus
}
#endif

#endif // BMW_PID_ENTRY_H
