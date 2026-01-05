
import argparse
import sys
import copy
import os
from utils.parser import parse_input
from utils.gantt import print_gantt_chart
from utils.statistics import StatsCalculator, save_graphs

from algorithms import fcfs, sjf, srtf, rr, priority_np, priority_p

# Mapping of algorithm names to their implementation modules
ALGORITHMS = {
    'FCFS': fcfs,
    'SJF': sjf,
    'SRTF': srtf,
    'RR': rr,
    'PRIO_NP': priority_np,
    'PRIO_P': priority_p
}

class Tee:
    
    # Helper class to redirect stdout to both console and a log file simultaneously.
    
    # This allows the program output to be visible to the user while also being saved to a file for later review or submission.
    
    def __init__(self, filename):
        # Initialize Tee with terminal and file handles.
        self.terminal = sys.stdout  # Original stdout (console)
        self.log = open(filename, "w")  # Output log file

    def write(self, message):
        # Write message to both terminal and log file.
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        # Flush both output streams.
        self.terminal.flush()
        self.log.flush()
        
    def close(self):
        # Close the log file.
        self.log.close()

def generate_execution_log(processes, execution_log):
    
   # Generates a detailed chronological text log of all scheduling events.
    
   # Events include:
   # - Process arrivals
   # - Process starts running
   # - Process completions
    
   # Args:
   # processes: List of process dictionaries (used for arrival times and completion checking)
   # execution_log: List of (start, end, pid) tuples from the scheduling algorithm
        
    # Returns:
    #    List of (time, event_message) tuples sorted chronologically
    
    events = []
    
    # Add all process arrival events
    for p in processes:
        events.append((p['arrival_time'], f"{p['pid']} arrives"))
        
    # Track previous process to detect context switches
    last_pid = None
    
    # Sort execution log by start time to ensure correct ordering
    execution_log.sort(key=lambda x: x[0])
    
    # Process each execution block
    for start, end, pid in execution_log:
        # Context switch detection (for logging purposes)
        if last_pid is not None and last_pid != pid:
            # Process changed - this is a context switch or preemption
            pass
            
        # Record when this process starts running
        events.append((start, f"{pid} starts running"))
        
        # Check if this process completed at the end of this block
        # Find the process object to check completion time
        proc = next((p for p in processes if p['pid'] == pid), None)
        if proc and proc['completion_time'] == end:
             events.append((end, f"{pid} completes"))
             
        last_pid = pid

    # Define priority for event ordering when multiple events occur at same time
    # Priority order: Arrival -> Completion -> Start (logical real-world order)
    def event_priority(msg):
        # Helper function to determine event priority for tie-breaking.
        if "arrives" in msg: return 0  # Arrivals happen first
        if "completes" in msg: return 1  # Then completions
        if "starts" in msg: return 2  # Then starts
        return 3
        
    # Sort events by time, then by priority
    events.sort(key=lambda x: (x[0], event_priority(x[1])))
    
    # Print formatted execution log
    print("\nExecution Log:")
    for time, msg in events:
        print(f"t={time}: {msg}")
        
    return events

def run_algorithm(algo_name, processes, quantum=None):
    # Executes a single scheduling algorithm and displays all results.
# 
# Steps:
# 1. Run the scheduling algorithm
# 2. Generate and display Gantt chart
# 3. Generate and display execution log
# 4. Calculate context switches
# 5. Calculate and display performance statistics
# 
# Args:
#     algo_name: Name of the algorithm (e.g., 'FCFS', 'RR')
#     processes: List of process dictionaries
#     quantum: Time quantum (required only for Round Robin)
#     
# Returns:
#     Tuple of (metrics_dict, processes_list) or (None, None) on error

    print(f"--- Running {algo_name} ---")
    
    # Deep copy to avoid modifying original process data
    proc_copy = copy.deepcopy(processes)
    
    # Execute the scheduling algorithm
    if algo_name == 'RR':
        # Round Robin requires quantum parameter
        if quantum is None:
            print("Error: Quantum required for RR.")
            return None, None
        execution_log = ALGORITHMS[algo_name].schedule(proc_copy, quantum)
    else:
        # Other algorithms don't need quantum
        execution_log = ALGORITHMS[algo_name].schedule(proc_copy)
        
    # Display visual Gantt chart
    print_gantt_chart(execution_log)
    
    # Display detailed event log
    generate_execution_log(proc_copy, execution_log)
    
    # Calculate context switches (number of CPU switches between processes)
    context_switches = 0
    if len(execution_log) > 0:
        execution_log_sorted = sorted(execution_log, key=lambda x: x[0])
        # Count switches: when PID changes between consecutive blocks
        for i in range(1, len(execution_log_sorted)):
            if execution_log_sorted[i][2] != execution_log_sorted[i-1][2]:
                context_switches += 1
    
    print(f"\nTotal Context Switches: {context_switches}")
    
    # Calculate performance metrics (turnaround, waiting, response times)
    stats_calc = StatsCalculator(proc_copy)
    metrics = stats_calc.compute_metrics()
    metrics['context_switches'] = context_switches
    
    return metrics, proc_copy

def main():
    parser = argparse.ArgumentParser(description="CPU Process Scheduling Simulator")
    parser.add_argument('--input', required=True, help="Path to process description file")
    parser.add_argument('--algo', required=True, help="Algorithm to run: FCFS, SJF, SRTF, RR, PRIO_NP, PRIO_P, or ALL")
    parser.add_argument('--quantum', type=int, help="Time quantum for RR")
    parser.add_argument('--output', help="Optional output file to save logs")
    
    args = parser.parse_args()
    
    # Redirect stdout if output file is specified
    original_stdout = sys.stdout
    tee = None
    if args.output:
        tee = Tee(args.output)
        sys.stdout = tee
    
    try:
        processes = parse_input(args.input)
        if not processes:
            sys.exit(1)
            
        if args.algo == 'ALL':
            results = {}
            print(f"Running ALL algorithms on {args.input}...\n")
            
            for name in ALGORITHMS.keys():
                q = args.quantum if args.quantum else 2
                metrics, _ = run_algorithm(name, processes, q)
                if metrics:
                    results[name] = metrics
                print("-" * 50)
                
            print("\nAlgorithm Comparison Summary:")
            print(f"{'Algorithm':<10} {'Avg Turnaround':<15} {'Avg Waiting':<15} {'Avg Response':<15} {'Context Switches':<18}")
            for name, metrics in results.items():
                ctx_switches = metrics.get('context_switches', 0)
                print(f"{name:<10} {metrics['avg_turnaround']:<15.2f} {metrics['avg_waiting']:<15.2f} {metrics['avg_response']:<15.2f} {ctx_switches:<18}")
                
            save_graphs(results)
            
        elif args.algo in ALGORITHMS:
            run_algorithm(args.algo, processes, args.quantum)
        else:
            print(f"Unknown algorithm: {args.algo}")
            sys.exit(1)
            
    finally:
        if tee:
            sys.stdout = original_stdout
            tee.close()

if __name__ == "__main__":
    main()
