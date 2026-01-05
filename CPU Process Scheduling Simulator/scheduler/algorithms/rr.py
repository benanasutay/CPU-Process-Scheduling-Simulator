from collections import deque

def schedule(processes, quantum):
   # Round Robin (RR) - Preemptive Scheduling Algorithm.
# 
# Each process gets a fixed time slice (quantum). If not completed, it goes
# to the back of the ready queue. Provides good response time and fairness.
# 
# Args:
#     processes: List of process dictionaries with 'arrival_time', 'burst_time', 'pid'
#     quantum: Time slice allocated to each process
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
        
    # Sort by arrival time for initial processing
    processes.sort(key=lambda x: (x['arrival_time'], x['pid']))
    
    queue = deque()  # Ready queue (FIFO for RR)
    added_to_queue = set()  # Track which processes are already queued
    
    def add_new_arrivals(time):
        # Helper function: Add all processes that have arrived by given time to the queue.
        for p in processes:
            if p['arrival_time'] <= time and p['pid'] not in added_to_queue:
                queue.append(p)
                added_to_queue.add(p['pid'])
                
    # Add processes that arrive at time 0
    add_new_arrivals(current_time)
    
    # Continue until all processes are completed
    while completed < n:
        if not queue:
            # Queue is empty but processes remain - CPU is idle
            # Fast-forward to next process arrival
            remaining = [p for p in processes if not p['completed']]
            if remaining:
                next_arrival = min(p['arrival_time'] for p in remaining)
                current_time = next_arrival
                add_new_arrivals(current_time)
            else:
                break
                
        # Get next process from front of queue
        current_process = queue.popleft()
        
        # Record first start time (for response time calculation)
        if current_process['start_time'] is None:
            current_process['start_time'] = current_time
            
        # Execute for quantum or remaining time, whichever is smaller
        exec_time = min(quantum, current_process['remaining_time'])
        
        start_block = current_time
        current_time += exec_time
        current_process['remaining_time'] -= exec_time
        
        # Log this execution block
        execution_log.append((start_block, current_time, current_process['pid']))
        
        # Add any processes that arrived while this process was executing
        # Important: New arrivals are added BEFORE re-adding current process (fairness)
        add_new_arrivals(current_time)
        
        # Check if process is complete or needs more time
        if current_process['remaining_time'] > 0:
            # Not finished - send to back of queue for next turn
            queue.append(current_process)
        else:
            # Process completed
            current_process['completed'] = True
            current_process['completion_time'] = current_time
            completed += 1
            
    return execution_log

