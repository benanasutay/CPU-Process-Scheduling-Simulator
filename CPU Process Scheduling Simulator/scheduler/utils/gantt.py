def print_gantt_chart(execution_log):
    # Generates and prints an ASCII Gantt chart visualization of process execution.
# 
# The Gantt chart shows:
# - Time markers along the top
# - Process IDs in blocks representing when each process ran
# - Idle periods (if any) shown as dashes
# 
# Args:
#     execution_log: List of tuples (start_time, end_time, pid) representing execution blocks
    if not execution_log:
        print("No execution log to display.")
        return

    print("\nGantt Chart:")
    
    # Calculate total simulation time (end of last process)
    total_time = execution_log[-1][1]
    
    # Print time markers at the top
    # Format: Time: 0  1  2  3  4  ...
    time_str = "Time: "
    for i in range(total_time + 1):
        time_str += f"{i:<3}"  # Each time unit takes 3 characters
    print(time_str)
    
    # Build the process execution bar
    bar_str = "|"
    current_time = 0
    
    for start, end, pid in execution_log:
        # Handle CPU idle time (gap between processes)
        if start > current_time:
            idle_duration = start - current_time
            bar_str += "-" * (idle_duration * 3) + "|"  # 3 chars per time unit
            
        # Create process execution block
        duration = end - start
        block_width = duration * 3  # Width in characters
        pid_str = f"{pid}"
        
        # Center the PID within the block
        padding = block_width - len(pid_str)
        left_pad = padding // 2
        right_pad = padding - left_pad
        
        bar_str += "-" * left_pad + pid_str + "-" * right_pad + "|"
        current_time = end
        
    print(bar_str)
    print()

