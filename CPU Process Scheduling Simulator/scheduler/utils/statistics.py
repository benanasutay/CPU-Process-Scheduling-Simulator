import matplotlib.pyplot as plt
import os

class StatsCalculator:
    
# Calculates and displays process scheduling statistics.
# Computes performance metrics for each process and overall averages:
# Turnaround Time: Total time from arrival to completion
# Waiting Time: Time spent waiting in ready queue
# Response Time: Time from arrival to first CPU access
    
    def __init__(self, processes):
        
        # Initialize the calculator with process data.
        
        # Args: processes: List of process dicts with computed times (completion_time, start_time)
        
        self.processes = processes

    def compute_metrics(self):
        
        # Computes performance metrics for each process and calculates averages.
        
        # Formulas:
        #    Turnaround Time = Completion Time - Arrival Time
        #    Waiting Time = Turnaround Time - Burst Time
        #    Response Time = First Start Time - Arrival Time
        
        # Returns:
           # Dictionary containing:
           # - avg_turnaround: Average turnaround time across all processes
           #    - avg_waiting: Average waiting time across all processes
           #    - avg_response: Average response time across all processes
        
        total_turnaround = 0
        total_waiting = 0
        total_response = 0
        n = len(self.processes)
        
        # Print table header
        print("\nPer-Process Statistics:")
        print(f"{'PID':<5} {'Arr':<5} {'Burst':<6} {'Compl':<6} {'Turn':<6} {'Wait':<6} {'Resp':<6}")
        
        # Calculate metrics for each process
        for p in self.processes:
            # Turnaround Time = time from arrival to completion
            p['turnaround_time'] = p['completion_time'] - p['arrival_time']
            
            # Waiting Time = turnaround minus actual CPU usage
            p['waiting_time'] = p['turnaround_time'] - p['burst_time']
            
            # Response Time = time from arrival to first CPU access
            p['response_time'] = p['start_time'] - p['arrival_time']
            
            # Accumulate totals for averaging
            total_turnaround += p['turnaround_time']
            total_waiting += p['waiting_time']
            total_response += p['response_time']
            
            # Print per-process statistics
            print(f"{p['pid']:<5} {p['arrival_time']:<5} {p['burst_time']:<6} {p['completion_time']:<6} {p['turnaround_time']:<6} {p['waiting_time']:<6} {p['response_time']:<6}")
        
        # Calculate averages
        avg_turnaround = total_turnaround / n
        avg_waiting = total_waiting / n
        avg_response = total_response / n
        
        # Print average statistics
        print(f"\nAverages:")
        print(f"Turnaround: {avg_turnaround:.2f}")
        print(f"Waiting: {avg_waiting:.2f}")
        print(f"Response: {avg_response:.2f}")
        
        return {
            'avg_turnaround': avg_turnaround,
            'avg_waiting': avg_waiting,
            'avg_response': avg_response
        }

def save_graphs(results, output_dir="graphs"):
    
    # Generates and saves comparison bar charts for algorithm performance.
    
    # Creates two graphs:
    # 1. Average Waiting Time vs Algorithm
    # 2. Average Turnaround Time vs Algorithm
    
    # Args:
    #  results: Dictionary mapping algorithm names to their metrics
    #             Format: {'FCFS': {'avg_waiting': 8.75, 'avg_turnaround': 15.25, ...}, ...}
    #    output_dir: Directory to save graphs (default: "graphs")
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # Extract data for plotting
    algorithms = list(results.keys())  # Algorithm names (x-axis labels)
    avg_waiting = [results[algo]['avg_waiting'] for algo in algorithms]  # Waiting time values
    avg_turnaround = [results[algo]['avg_turnaround'] for algo in algorithms]  # Turnaround time values
    
    # Generate Waiting Time Bar Chart
    plt.figure(figsize=(10, 6))
    plt.bar(algorithms, avg_waiting, color='skyblue')
    plt.xlabel("Algorithm")
    plt.ylabel("Average Waiting Time")
    plt.title("Average Waiting Time vs Algorithm")
    plt.savefig(os.path.join(output_dir, "waiting_time.png"))  # Save to file
    plt.close()  # Close figure to free memory
    
    # Generate Turnaround Time Bar Chart
    plt.figure(figsize=(10, 6))
    plt.bar(algorithms, avg_turnaround, color='salmon')
    plt.xlabel("Algorithm")
    plt.ylabel("Average Turnaround Time")
    plt.title("Average Turnaround Time vs Algorithm")
    plt.savefig(os.path.join(output_dir, "turnaround_time.png"))  # Save to file
    plt.close()  # Close figure to free memory
    
    print(f"\nGraphs saved to {output_dir}/")

