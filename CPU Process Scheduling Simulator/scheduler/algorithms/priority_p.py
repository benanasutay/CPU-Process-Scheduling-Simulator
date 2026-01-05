def schedule(processes):
    # Priority Scheduling (Preemptive) Algorithm.
# 
# If a process arrives with higher priority than the currently running process,
# it preempts the CPU. Important processes get immediate CPU access.
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
    
    # Initialize remaining time for each process
    for p in processes:
        p['remaining_time'] = p['burst_time']  # Track how much time is left
        p['completed'] = False
        p['start_time'] = None  # Will be set on first CPU access
        
    last_pid = None  # Track which process was running previously
    start_of_block = 0  # When current execution block started
    
    # Continue until all processes are completed
    while completed < n:
        # Find all available processes (arrived and not completed)
        available = [p for p in processes if p['arrival_time'] <= current_time and not p['completed']]
        
        if not available:
            # No process available - CPU idle, advance time
            current_time += 1
            continue
            
        # Select process with highest priority (lowest numeric value)
        # Tie-breaker: arrival time first, then process ID
        highest_prio = min(available, key=lambda x: (x['priority'], x['arrival_time'], x['pid']))
        
        # Record first start time (for response time calculation)
        if highest_prio['start_time'] is None:
            highest_prio['start_time'] = current_time
            
        # Check if we need to switch processes (context switch due to preemption)
        if highest_prio['pid'] != last_pid:
            if last_pid is not None:
                # Close the previous execution block
                execution_log.append((start_of_block, current_time, last_pid))
            # Start new block
            start_of_block = current_time
            last_pid = highest_prio['pid']
            
        # Execute process for 1 time unit
        highest_prio['remaining_time'] -= 1
        current_time += 1
        
        # Check if process completed
        if highest_prio['remaining_time'] == 0:
            highest_prio['completed'] = True
            highest_prio['completion_time'] = current_time
            completed += 1
            
    # Append the final execution block
    if last_pid is not None:
        execution_log.append((start_of_block, current_time, last_pid))
        
    return execution_log

