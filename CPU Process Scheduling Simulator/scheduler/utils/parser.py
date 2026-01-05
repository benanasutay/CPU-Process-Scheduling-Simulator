def parse_input(filename):
    # Parses the process input file and creates a list of process dictionaries.
# 
# Expected File Format:
#     # Comments start with #
#     PID arrival_time burst_time priority
#     P1  0            8          2
# 
# Args:
#     filename: Path to the input file
# 
# Returns:
#     List of process dictionaries, each containing:
#         - pid: Process identifier (string)
#         - arrival_time: When process arrives (integer)
#         - burst_time: CPU time required (integer)
#         - priority: Process priority, lower = higher priority (integer)
#         - remaining_time: Initialized to burst_time, used by preemptive algorithms
#         - start_time: When process first gets CPU (None initially)
#         - completion_time: When process finishes execution (0 initially)
    processes = []
    
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()  # Remove leading/trailing whitespace
                
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                
                # Parse process data
                parts = line.split()
                if len(parts) != 4:  # Expecting exactly 4 fields
                    continue
                
                pid = parts[0]  # Process ID (string)
                arrival_time = int(parts[1])  # Arrival time (convert to int)
                burst_time = int(parts[2])  # Burst time (convert to int)
                priority = int(parts[3])  # Priority (convert to int)
                
                # Create process dictionary with all necessary fields
                processes.append({
                    'pid': pid,
                    'arrival_time': arrival_time,
                    'burst_time': burst_time,
                    'priority': priority,
                    'remaining_time': burst_time,  # For preemptive algorithms
                    'start_time': None,  # Will be set when process first runs
                    'completion_time': 0  # Will be set when process finishes
                })
                
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        return []
    except ValueError:
        print(f"Error: Invalid number format in {filename}.")
        return []
        
    # Sort processes by arrival time for initial ordering
    processes.sort(key=lambda x: x['arrival_time'])
    return processes

