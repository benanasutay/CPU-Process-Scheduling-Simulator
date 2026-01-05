# CPU Process Scheduling Simulator

# 2. Overview
This project is a high-fidelity CPU Process Scheduling Simulator developed in Python 3. It models how an operating system manages process execution on a single-core CPU using various classical scheduling strategies.

# Key Features:

ASCII Gantt Charts: Dynamic visual representation of CPU allocation.

Detailed Execution Logs: Step-by-step chronological event tracking.

Automated Metrics: Calculation of Waiting Time, Turnaround Time, Response Time, and Context Switch counts.

Data Visualization: Comparative performance graphs generated via matplotlib.

# 3. Environment & Dependencies
Python Version: 3.x (Recommended 3.10+)

Standard Libraries: argparse, sys: For command-line argument handling.

collections.deque: Used for efficient queue management in Round Robin.

copy: Ensures original process data remains intact during simulations.

External Libraries: matplotlib: Required for generating statistical graphs.

# Installation
To install the necessary external dependency, run:

pip install matplotlib

# 4. How to Run the Simulator
The simulator is driven by the scheduler.py script. It requires an input file (e.g., processes.txt) and an algorithm flag.

# General Syntax

python scheduler.py --input <filename> --algo <ALGORITHM> [--quantum <value>]

# Sample Commands
1. First-Come First-Served: python scheduler.py --input processes.txt --algo FCFS

2. Shortest Remaining Time First: python scheduler.py --input processes.txt --algo SRTF

3. Round Robin (Quantum = 2): python scheduler.py --input processes.txt --algo RR --quantum 2

4. Run All & Compare Performance: python scheduler.py --input processes.txt --algo ALL --quantum 2 (Generates waiting_time.png and turnaround_time.png in the graphs/ directory).

# 5. Algorithm Implementation Logic
Each algorithm handles ties deterministically by PID order and strictly respects arrival times:

FCFS (First-Come First-Served): A non-preemptive approach where processes are executed based on their arrival.

SJF (Shortest Job First): A non-preemptive algorithm that selects the available process with the smallest total burst time.

SRTF (Shortest Remaining Time First): A preemptive version of SJF. It uses a unit-step simulation to re-evaluate at every clock tick if a new arrival has a shorter remaining time than the current job.

RR (Round Robin): A preemptive, time-sliced algorithm using a deque (FIFO queue). New arrivals are added to the queue before re-adding a preempted process to ensure fair distribution.

Priority (Non-Preemptive): Executes the highest-priority job (lowest integer value) to completion.

Priority (Preemptive): Immediately interrupts the current process if a higher-priority job arrives.

# 6. Discussion of Results
The following observations are based on the simulation results generated using the provided `processes.txt` workload. The analysis focuses on performance metrics, trade-offs, and system behavior.

# Best Performing Algorithm: SRTF
* **Overall Winner:** **SRTF** (Shortest Remaining Time First)
* **Metrics:** It achieved the lowest **Average Waiting Time (6.50)** and **Average Turnaround Time (13.00)**.
* **Reasoning:** Since SRTF continually prioritizes the process closest to completion, it clears processes from the queue faster than any other algorithm. This minimizes the time other processes spend in the "Ready" state.
* **Runner-Up:** **PRIO_P** also performed impressively (Avg Waiting: 7.00), demonstrating that preemption is highly effective for delivering better response times in priority-based tasks.

# Observations & Trade-offs
# 1. Round Robin (RR) Overhead
* **The Trade-off:** With a time quantum of 2, RR produced the **worst Average Turnaround Time (19.25)** and **Waiting Time (12.75)**.
* **The "Ping-Pong" Effect:** The most notable observation was the high frequency of Context Switches. RR required 12 switches, whereas other algorithms only needed 3 or 4. This highlights the significant overhead cost associated with fair, time-sliced scheduling.
* **The Benefit:** Despite these costs, RR provided the best **Average Response Time (2.00)**. This confirms that while inefficient for batch processing speed, RR is superior for interactive environments where immediate initial feedback is critical.

# 2. Impact of Preemption
* **Interactive vs. Batch:** Preemptive algorithms (SRTF, PRIO_P) consistently provided better **Response Times** than their non-preemptive counterparts (SJF, PRIO_NP).
* **Conclusion:** This makes preemptive strategies much more suitable for interactive systems where user responsiveness is a priority, whereas non-preemptive algorithms are better for reducing context switch overhead.

# Surprising Behaviours & Observations
High Round Robin Overhead: RR with a quantum of 2 resulted in the worst Average Turnaround Time (19.25).

The "Ping-Pong" Effect: The most notable observation was the high frequency of Context Switches. RR performed 12 switches, while other algorithms required only 3 or 4. This clearly demonstrates the significant overhead cost incurred by frequent preemption in systems with small time slices.

Performance Trade-off: While RR was inefficient for turnaround time, it provided the best Average Response Time (2.00). This confirms that Round Robin is superior for interactive environments where rapid initial feedback to the user is more critical than total completion speed.

# 7. Project Structure

scheduler/
├── scheduler.py           # Main driver and CLI
├── processes.txt          # Input workload file
├── algorithms/            # Implementation of logic
│   ├── fcfs.py
│   ├── sjf.py
│   ├── srtf.py
│   ├── rr.py
│   ├── priority_np.py
│   └── priority_p.py
└── utils/                 # Helper modules
    ├── parser.py          # Input parsing logic
    ├── gantt.py           # ASCII Gantt chart generation
    └── statistics.py      # Calculations and graph generation