def schedule(processes):
    # Priority Scheduling (Non-preemptive) Algorithm.
# 
# Selects the process with highest priority (lowest numeric value).
# Important processes run first, but low priority processes may starve.
# 
# Priority Convention: Lower integer value = Higher priority
# 
# Args:
#     processes: List of process dictionaries with 'arrival_time', 'burst_time', 'priority', 'pid'
# 
# Returns:
#     execution_log: List of tuples (start_time, end_time, pid) representing execution blocks
    current_time = 0  # Tracks current system time
    completed = 0  # Number of completed processes
    n = len(processes)  # Total number of processes
    execution_log = []  # Stores execution history
    
    # Initialize completion status
    for p in processes:
        p['completed'] = False
        
    # Continue until all processes are completed
    while completed < n:
        # Find all available processes (arrived and not completed)
        available = [p for p in processes if p['arrival_time'] <= current_time and not p.get('completed', False)]
        
        if not available:
            # No process available - CPU idle, fast-forward to next arrival
            next_arrival = min(p['arrival_time'] for p in processes if not p.get('completed', False))
            current_time = next_arrival
            continue
            
        # Select process with highest priority (lowest numeric value)
        # Tie-breaker: arrival time first, then process ID
        highest_prio = min(available, key=lambda x: (x['priority'], x['arrival_time'], x['pid']))
        
        # Record start time (for response time calculation)
        start_time = current_time
        highest_prio['start_time'] = start_time
        
        # Execute process to completion (non-preemptive)
        current_time += highest_prio['burst_time']
        highest_prio['completion_time'] = current_time
        highest_prio['completed'] = True
        completed += 1
        
        # Log this execution block
        execution_log.append((start_time, current_time, highest_prio['pid']))
        
    return execution_log

