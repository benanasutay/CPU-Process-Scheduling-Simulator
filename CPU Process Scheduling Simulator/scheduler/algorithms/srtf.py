def schedule(processes):
   # Shortest Remaining Time First (SRTF) - Preemptive SJF Algorithm.
# 
# Preemptive version of SJF. If a new process arrives with shorter remaining time
# than the currently running process, it preempts the CPU. Minimizes average waiting time.
# 
# Args:
#     processes: List of process dictionaries with 'arrival_time', 'burst_time', 'pid'
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
        
    # Time-step simulation for accurate preemption handling
    # Note: Could be optimized using event-driven approach, but unit-step
    # is simpler and guarantees correctness for preemptive scheduling
    
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
            
        # Select process with shortest remaining time (SRTF policy)
        # Tie-breaker: arrival time first, then process ID
        shortest = min(available, key=lambda x: (x['remaining_time'], x['arrival_time'], x['pid']))
        
        # Record first start time (for response time calculation)
        if shortest['start_time'] is None:
            shortest['start_time'] = current_time
            
        # Check if we need to switch processes (context switch)
        if shortest['pid'] != last_pid:
            if last_pid is not None:
                # Close the previous execution block
                execution_log.append((start_of_block, current_time, last_pid))
            # Start new block
            start_of_block = current_time
            last_pid = shortest['pid']
            
        # Execute process for 1 time unit
        shortest['remaining_time'] -= 1
        current_time += 1
        
        # Check if process completed
        if shortest['remaining_time'] == 0:
            shortest['completed'] = True
            shortest['completion_time'] = current_time
            completed += 1
            
    # Append the final execution block
    if last_pid is not None:
        execution_log.append((start_of_block, current_time, last_pid))
        
    return execution_log

