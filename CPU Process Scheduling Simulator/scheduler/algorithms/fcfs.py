def schedule(processes):
    # First-Come First-Served (FCFS) Scheduling Algorithm.
# 
# This is a non-preemptive scheduling algorithm where processes are executed
# in the order they arrive. Simple but can suffer from the convoy effect.
# 
# Args:
#     processes: List of process dictionaries with 'arrival_time', 'burst_time', 'pid'
# 
# Returns:
#     execution_log: List of tuples (start_time, end_time, pid) representing execution blocks
    current_time = 0  # Tracks the current system time
    execution_log = []  # Stores execution history as (start, end, pid) tuples
    
    # Sort processes by arrival time, then by PID for deterministic tie-breaking
    processes.sort(key=lambda x: (x['arrival_time'], x['pid']))
    
    # Execute each process in order
    for p in processes:
        # If CPU is idle, fast-forward to process arrival time
        if current_time < p['arrival_time']:
            current_time = p['arrival_time']
            
        # Record when this process first gets CPU (for response time calculation)
        start_time = current_time
        p['start_time'] = start_time
        
        # Execute process to completion (non-preemptive)
        current_time += p['burst_time']
        p['completion_time'] = current_time
        
        # Log this execution block
        execution_log.append((start_time, current_time, p['pid']))
        
    return execution_log

