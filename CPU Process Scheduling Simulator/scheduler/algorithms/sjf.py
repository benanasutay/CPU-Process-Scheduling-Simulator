def schedule(processes):
    # Shortest Job First (SJF) - Non-preemptive Scheduling Algorithm.
# 
# Selects the process with the shortest burst time among available processes.
# Minimizes average waiting time but can cause starvation for long processes.
# 
# Args:
#     processes: List of process dictionaries with 'arrival_time', 'burst_time', 'pid'
# 
# Returns:
#     execution_log: List of tuples (start_time, end_time, pid) representing execution blocks
    current_time = 0  # Tracks the current system time
    completed = 0  # Number of processes completed
    n = len(processes)  # Total number of processes
    execution_log = []  # Stores execution history
    
    # Initialize completion status for all processes
    for p in processes:
        p['completed'] = False
        
    # Continue until all processes are completed
    while completed < n:
        # Find all processes that have arrived and are not yet completed
        available = [p for p in processes if p['arrival_time'] <= current_time and not p.get('completed', False)]
        
        if not available:
            # No process available right now - CPU is idle
            # Fast-forward to the next process arrival time
            next_arrival = min(p['arrival_time'] for p in processes if not p.get('completed', False))
            current_time = next_arrival
            continue
            
        # Select the process with shortest burst time (SJF policy)
        # Tie-breaker: arrival time first, then process ID
        shortest = min(available, key=lambda x: (x['burst_time'], x['arrival_time'], x['pid']))
        
        # Record start time (for response time calculation)
        start_time = current_time
        shortest['start_time'] = start_time
        
        # Execute process to completion (non-preemptive)
        current_time += shortest['burst_time']
        shortest['completion_time'] = current_time
        shortest['completed'] = True
        completed += 1
        
        # Log this execution block
        execution_log.append((start_time, current_time, shortest['pid']))
        
    return execution_log

